import 'package:dio/dio.dart';
import '../models/auth.dart';
import '../models/user.dart';
import 'api_base.dart';

class ApiAuth extends ApiBase {

  Future<LoginResponse> login({
    required String email,
    required String password,
  }) async {
    final Response<dynamic> response = await dio.post(
      '/auth/login',
      data: <String, String>{
        'username': email,
        'password': password,
      },
      options: Options(
        contentType: Headers.formUrlEncodedContentType,
      ),
    );

    return LoginResponse.fromJson(response.data);
  }

  Future<UserModel> register({
    required String email,
    required String password,
  }) async {
    final Response<dynamic> response = await dio.post(
      '/auth/register',
      data: <String, String>{
        'email': email,
        'password': password,
      },
    );

    return UserModel.fromJson(response.data);
  }
}