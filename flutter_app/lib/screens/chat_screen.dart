import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/chat_provider.dart';
import '../widgets/chat_message_bubble.dart';

class ChatScreen extends StatefulWidget {
  const ChatScreen({super.key});

  @override
  State<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  final TextEditingController _textController = TextEditingController();
  final ScrollController _scrollController = ScrollController();

  void _sendMessage() {
    final chatProvider = Provider.of<ChatProvider>(context, listen: false);
    if (_textController.text.isNotEmpty) {
      chatProvider.sendMessage(_textController.text);
      _textController.clear();
    }
  }

  Future<void> _showClearHistoryConfirmationDialog() async {
    return showDialog<void>(
      context: context,
      barrierDismissible: false, // User must tap a button.
      builder: (BuildContext dialogContext) {
        return AlertDialog(
          title: const Text('Clear Chat History'),
          content: const SingleChildScrollView(
            child: ListBody(
              children: <Widget>[
                Text('Are you sure you want to delete your entire chat history?'),
                Text('This action cannot be undone.'),
              ],
            ),
          ),
          actions: <Widget>[
            TextButton(
              child: const Text('Cancel'),
              onPressed: () {
                Navigator.of(dialogContext).pop();
              },
            ),
            TextButton(
              child: const Text('Clear'),
              onPressed: () {
                Provider.of<ChatProvider>(context, listen: false).clearChatHistory();
                Navigator.of(dialogContext).pop();
              },
            ),
          ],
        );
      },
    );
  }

  @override
  void dispose() {
    _textController.dispose();
    _scrollController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('AI Tutor & Assistant'),
        backgroundColor: Theme.of(context).colorScheme.surfaceVariant,
        actions: [
          Consumer<ChatProvider>(
            builder: (context, provider, child) {
              return DropdownButton<String>(
                value: provider.currentLanguage,
                underline: Container(), // Hides the default underline
                onChanged: (String? newValue) {
                  if (newValue != null) {
                    provider.setLanguage(newValue);
                  }
                },
                items: <String>['en-US', 'ur-PK']
                    .map<DropdownMenuItem<String>>((String value) {
                  return DropdownMenuItem<String>(
                    value: value,
                    child: Text(value == 'en-US' ? 'EN' : 'UR'),
                  );
                }).toList(),
              );
            },
          ),
          IconButton(
            icon: const Icon(Icons.delete_sweep_outlined),
            tooltip: 'Clear History',
            onPressed: _showClearHistoryConfirmationDialog,
          ),
          const SizedBox(width: 8),
        ],
      ),
      body: Column(
        children: [
          Expanded(
            child: Consumer<ChatProvider>(
              builder: (context, chatProvider, child) {
                final messages = chatProvider.messages;
                return ListView.builder(
                  controller: _scrollController,
                  reverse: true, // This is key for chat UIs
                  padding: const EdgeInsets.symmetric(vertical: 8.0),
                  itemCount: messages.length,
                  itemBuilder: (context, index) {
                    final message = messages[index];
                    return ChatMessageBubble(message: message);
                  },
                );
              },
            ),
          ),
          _buildTextInput(),
        ],
      ),
    );
  }

  Widget _buildTextInput() {
    final chatProvider = Provider.of<ChatProvider>(context, listen: true);
    return Material(
      elevation: 8.0,
      child: Padding(
        padding: EdgeInsets.only(
          left: 16.0,
          right: 8.0,
          top: 8.0,
          bottom: MediaQuery.of(context).viewInsets.bottom + 16.0,
        ),
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.end,
          children: [
            Expanded(
              child: TextField(
                controller: _textController,
                minLines: 1,
                maxLines: 5,
                decoration: InputDecoration(
                  hintText: 'Type your question...',
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(24.0),
                    borderSide: BorderSide.none,
                  ),
                  contentPadding: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
                  filled: true,
                  fillColor: Theme.of(context).colorScheme.surfaceVariant,
                  suffixIcon: IconButton(
                    icon: const Icon(Icons.attach_file),
                    onPressed: () => Provider.of<ChatProvider>(context, listen: false).sendFile(),
                  ),
                ),
                onSubmitted: chatProvider.isLoading ? null : (_) => _sendMessage(),
              ),
            ),
            const SizedBox(width: 8.0),
            chatProvider.isLoading
                ? IconButton(
                    icon: const Icon(Icons.stop_circle_outlined),
                    onPressed: () =>
                        Provider.of<ChatProvider>(context, listen: false)
                            .stopGeneration(),
                    style: IconButton.styleFrom(
                      backgroundColor: Theme.of(context).colorScheme.errorContainer,
                      foregroundColor:
                          Theme.of(context).colorScheme.onErrorContainer,
                    ),
                  )
                : IconButton(
                    icon: const Icon(Icons.send),
                    onPressed: _sendMessage,
                    style: IconButton.styleFrom(
                      backgroundColor: Theme.of(context).colorScheme.primary,
                      foregroundColor: Theme.of(context).colorScheme.onPrimary,
                    ),
                  ),
          ],
        ),
      ),
    );
  }
}