import 'package:flutter/material.dart';
import 'dart:async';
import 'package:uuid/uuid.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:image_picker/image_picker.dart';
import '../models/chat_message.dart';
import '../services/api_service.dart';

class ChatProvider with ChangeNotifier {
  final ApiService _apiService = ApiService();
  final List<ChatMessage> _messages = [];
  bool _isLoading = false;
  final Uuid _uuid = const Uuid();
  String _currentLanguage = 'en-US';
  StreamSubscription? _currentSubscription;

  List<ChatMessage> get messages => _messages;
  bool get isLoading => _isLoading;
  String get currentLanguage => _currentLanguage;

  ChatProvider() {
    _initialize();
  }

  Future<void> _initialize() async {
    final prefs = await SharedPreferences.getInstance();
    _currentLanguage = prefs.getString('language') ?? 'en-US';
    notifyListeners();
  }

  Future<void> setLanguage(String languageCode) async {
    _currentLanguage = languageCode;
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('language', languageCode);
    notifyListeners();
  }

  void stopGeneration() {
    if (_currentSubscription != null) {
      _currentSubscription!.cancel();
      _currentSubscription = null;
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<void> clearChatHistory() async {
    try {
      await _apiService.clearHistory();
      _messages.clear();
      notifyListeners();
    } catch (e) {
      debugPrint("Failed to clear history: $e");
      // Optionally, you could set an error state here to show a snackbar in the UI.
    }
  }

  void _handleApiStream(Stream<String> apiStream) {
    _isLoading = true;
    notifyListeners();

    final aiMessageId = _uuid.v4();
    final aiMessage = ChatMessage(
      id: aiMessageId,
      text: '',
      author: MessageAuthor.ai,
      timestamp: DateTime.now(),
    );
    _messages.insert(0, aiMessage);

    _currentSubscription = apiStream.listen((chunk) {
      final index = _messages.indexWhere((msg) => msg.id == aiMessageId);
      if (index != -1) {
        final currentMessage = _messages[index];
        _messages[index] = ChatMessage(
            id: aiMessageId,
            text: currentMessage.text + chunk,
            author: MessageAuthor.ai,
            timestamp: currentMessage.timestamp);
        notifyListeners();
      }
    }, onDone: () {
      _isLoading = false;
      _currentSubscription = null;
      notifyListeners();
    }, onError: (error) {
      final index = _messages.indexWhere((msg) => msg.id == aiMessageId);
      if (index != -1) {
        _messages[index] = ChatMessage(
            id: aiMessageId,
            text: 'Error: $error',
            author: MessageAuthor.ai,
            timestamp: _messages[index].timestamp);
      }
      _isLoading = false;
      _currentSubscription = null;
      notifyListeners();
    });
  }

  void _handleApiStream(Stream<String> apiStream) {
    _isLoading = true;
    notifyListeners();

    final aiMessageId = _uuid.v4();
    final aiMessage = ChatMessage(
      id: aiMessageId,
      text: '',
      author: MessageAuthor.ai,
      timestamp: DateTime.now(),
    );
    _messages.insert(0, aiMessage);

    _currentSubscription = apiStream.listen((chunk) {
      final index = _messages.indexWhere((msg) => msg.id == aiMessageId);
      if (index != -1) {
        final currentMessage = _messages[index];
        _messages[index] = ChatMessage(
            id: aiMessageId,
            text: currentMessage.text + chunk,
            author: MessageAuthor.ai,
            timestamp: currentMessage.timestamp);
        notifyListeners();
      }
    }, onDone: () {
      _isLoading = false;
      _currentSubscription = null;
      notifyListeners();
    }, onError: (error) {
      // This part can be enhanced to show a more specific error message
      _isLoading = false;
      _currentSubscription = null;
      notifyListeners();
    });
  }

  Future<void> sendMessage(String text) async {
    if (text.isEmpty) return;

    // Add user message immediately to the start of the list
    final userMessage = ChatMessage(
      id: _uuid.v4(),
      text: text,
      author: MessageAuthor.user,
      timestamp: DateTime.now(),
    );
    _messages.insert(0, userMessage);
    _handleApiStream(_apiService.askTextStream(text, _currentLanguage));
  }

  Future<void> sendFile() async {
    final picker = ImagePicker();
    final XFile? image = await picker.pickImage(source: ImageSource.gallery);

    if (image == null) return;

    // Add a user message showing a file was sent
    final userMessage = ChatMessage(
      id: _uuid.v4(),
      text: 'Sent an image: ${image.name}',
      author: MessageAuthor.user,
      timestamp: DateTime.now(),
    );
    _messages.insert(0, userMessage);
    _handleApiStream(_apiService.askWithFile(image.path, _currentLanguage));
  }
}