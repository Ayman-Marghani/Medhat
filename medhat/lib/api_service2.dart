
import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  final String baseUrl;

  ApiService(this.baseUrl);

  Future<String> chatWithBot(String userInput) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/api?query=$userInput'),  // Updated endpoint for GET request
        headers: {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        Map<String, dynamic> responseData = jsonDecode(response.body);
        String chatbotResponse = responseData['output'];
        return chatbotResponse;
      } else {
        throw Exception('Failed to communicate with the chatbot server');
      }
    } catch (e) {
      throw Exception('Error: $e');
    }
  }
}
