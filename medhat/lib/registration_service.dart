import 'dart:convert';
import 'package:http/http.dart' as http;

class RegService {
  final String baseUrl;

  RegService(this.baseUrl);

  Future<String> registerUser({
    required String password,
    required String name,
    required String date_of_birth,
    required String gender,
    required String chronic_illness,
    required String username,
  }) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/register?password=$password&name=$name&date_of_birth=$date_of_birth&gender=$gender&chronic_illness=$chronic_illness&username=$username'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(<String, String>{
          'password': password,
          'name': name,
          'date_of_birth': date_of_birth,
          'gender': gender,
          'chronic_illness': chronic_illness,
          'username': username,
        }),
      );

      if (response.statusCode == 200) {
        print("received code 200");
        Map<String, dynamic> responseData = jsonDecode(response.body);
        print("in between");
        print(responseData);
        String message = responseData['message'];
        print("message: $message");
        print("about to return aho <<<");
        return message;
      } else {
        throw Exception('Failed to register user');
      }
    } catch (e) {
      print("error in registration.dart");
      throw Exception('Error: $e');
    }
  }
}
