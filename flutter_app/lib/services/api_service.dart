import 'dart:async';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import 'package:uuid/uuid.dart';

class ApiService {
  // Production URL for the deployed backend
  static const String _prodUrl = 'https://guidely-api.fly.dev';
  // For local development:
  // - Android Emulator: use 10.0.2.2 to connect to your local machine's localhost
  // - iOS Simulator: use localhost
  // - Physical devices: use your computer's network IP address
  static const String _devUrl = 'http://10.0.2.2:8000';
  
  // Set to true for production, false for development
  static const bool _isProduction = true;
  
  static String get _baseUrl => _isProduction ? _prodUrl : _devUrl;
  static String? _userId;

  Future<void> initialize() async {
    if (_userId != null) return;

    final prefs = await SharedPreferences.getInstance();
    var userId = prefs.getString('userId');
    if (userId == null) {
      userId = 'flutter-user-${const Uuid().v4()}';
      await prefs.setString('userId', userId);
    }
    _userId = userId;
  }

  Stream<String> askTextStream(String query, String language) async* {
    if (_userId == null) await initialize();

    final url = Uri.parse('$_baseUrl/ask-text-stream');

    final request = http.Request('POST', url)
      ..headers['Content-Type'] = 'application/json'
      ..body = jsonEncode({
        'query': query,
        'user_id': _userId!,
        'mode': 'tutor',
        'language': language,
      });

    try {
      final streamedResponse = await request.send();
      await for (var chunk in streamedResponse.stream.transform(utf8.decoder)) {
        yield chunk;
      }
    } catch (e) {
      yield 'Error: Could not connect to the server.';
    }
  }

  Stream<String> askWithFile(String filePath, String language) async* {
    if (_userId == null) await initialize();
    // The backend /ask-image endpoint is now streaming text/plain
    final url = Uri.parse('$_baseUrl/ask-image');

    final request = http.MultipartRequest('POST', url)
      ..fields['user_id'] = _userId!
      ..fields['mode'] = 'tutor'
      ..fields['language'] = language
      ..files.add(await http.MultipartFile.fromPath('file', filePath));

    try {
      final streamedResponse = await request.send();

      if (streamedResponse.statusCode == 200) {
        await for (var chunk in streamedResponse.stream.transform(utf8.decoder)) {
          yield chunk;
        }
      } else {
        final errorBody = await streamedResponse.stream.bytesToString();
        yield 'Error: ${streamedResponse.statusCode} - $errorBody';
      }
    } catch (e) {
      yield 'Error: Failed to process the file.';
    }
  }

  Future<void> clearHistory() async {
    if (_userId == null) await initialize();
    final url = Uri.parse('$_baseUrl/history/$_userId');
    final response = await http.delete(url);

    if (response.statusCode != 204) {
      throw Exception('Failed to clear history on the server.');
    }
  }
}