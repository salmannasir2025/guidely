enum MessageAuthor { user, ai }

class ChatMessage {
  final String id;
  final String text;
  final MessageAuthor author;
  final DateTime timestamp;

  ChatMessage({
    required this.id,
    required this.text,
    required this.author,
    required this.timestamp,
  });
}