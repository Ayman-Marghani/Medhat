import 'dart:convert';
import 'package:http/http.dart' as http;

class RetrieveService {
  final String baseUrl;

  RetrieveService(this.baseUrl);

  Future<Map<String, dynamic>> retrieveUserInfo({
    required String username,
  }) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/retrieve'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(<String, String>{
          'username': username,
        }),
      );

      if (response.statusCode == 200) {
        print("data retrieved");
        Map<String, dynamic> responseData = jsonDecode(response.body);
        return responseData;
      } else {
        throw Exception('Failed to retrieve user information');
      }
    } catch (e) {
      print("Error in retrieve_service.dart: $e");
      throw Exception('Error: $e');
    }
  }
}
