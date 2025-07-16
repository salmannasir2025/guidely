import 'package:flutter/material.dart';
import 'package:flutter_markdown/flutter_markdown.dart';
import '../models/chat_message.dart';

class ChatMessageBubble extends StatelessWidget {
  final ChatMessage message;

  const ChatMessageBubble({super.key, required this.message});

  @override
  Widget build(BuildContext context) {
    final isUser = message.author == MessageAuthor.user;
    final theme = Theme.of(context);

    return Align(
      alignment: isUser ? Alignment.centerRight : Alignment.centerLeft,
      child: Container(
        constraints: BoxConstraints(
          maxWidth: MediaQuery.of(context).size.width * 0.75,
        ),
        margin: const EdgeInsets.symmetric(vertical: 5.0, horizontal: 8.0),
        padding: const EdgeInsets.symmetric(vertical: 10.0, horizontal: 14.0),
        decoration: BoxDecoration(
          color: isUser ? theme.colorScheme.primary : theme.colorScheme.secondaryContainer,
          borderRadius: BorderRadius.only(
            topLeft: const Radius.circular(20.0),
            topRight: const Radius.circular(20.0),
            bottomLeft: isUser ? const Radius.circular(20.0) : Radius.zero,
            bottomRight: isUser ? Radius.zero : const Radius.circular(20.0),
          ),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            message.author == MessageAuthor.ai
                ? MarkdownBody(
                    data: message.text.isEmpty ? "..." : message.text,
                    styleSheet: MarkdownStyleSheet.fromTheme(theme).copyWith(
                      // Ensure all text elements within the markdown use the correct color
                      baseStyle: theme.textTheme.bodyMedium?.copyWith(
                        color: theme.colorScheme.onSecondaryContainer,
                      ),
                      p: theme.textTheme.bodyMedium?.copyWith(
                        color: theme.colorScheme.onSecondaryContainer,
                      ),
                    ),
                  )
                : Text(
                    message.text,
                    style: theme.textTheme.bodyMedium?.copyWith(color: Colors.white),
                  ),
          ],
        ),
      ),
    );
  }
}