/*
import 'dart:convert';
import 'package:http/http.dart' as http;

class LoginService {
  final String baseUrl;

  LoginService(this.baseUrl);

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
*/
import 'dart:convert';
import 'package:http/http.dart' as http;

class LoginService {
  final String baseUrl;

  LoginService(this.baseUrl);

  Future<String> loginUser({
    required String username,
    required String password,
  }) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/login?password=$password&username=$username'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(<String, String>{
          'username': username,
          'password': password,
        }),
      );

      if (response.statusCode == 200) {
        Map<String, dynamic> responseData = jsonDecode(response.body);
        print("responseData:\n $responseData!!");
        String message = responseData['message'];
        return message;
      } else {
        throw Exception('Failed to log in');
      }
    } catch (e) {
      print("error in login_service.dart");
      throw Exception('Error: $e');
    }
  }
}
