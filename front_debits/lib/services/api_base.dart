import 'package:dio/dio.dart';

class ApiBase {
  final Dio dio;

  ApiBase({
    String baseUrl = 'http://127.0.0.1:8000',
  }) : dio = Dio(
    BaseOptions(
      baseUrl: baseUrl,
      headers: {
        'Content-Type': 'application/json',
      },
    ),
  );

  void setToken(String token) {
    dio.options.headers['Authorization'] = 'Bearer $token';
  }

  void clearToken() {
    dio.options.headers.remove('Authorization');
  }
}

final ApiBase apiBase = ApiBase();