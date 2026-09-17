import 'package:awidgets/fields/a_field_email.dart';
import 'package:awidgets/fields/a_field_password.dart';
import 'package:awidgets/general/a_button.dart';
import 'package:awidgets/general/a_form.dart';
import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:front_debits/models/auth.dart';
import 'package:front_debits/widgets/page_card_layout.dart';

import '../../../core/default_colors.dart';
import '../services/api.dart';
import '../services/api_base.dart';
import 'home_page.dart';

class LoginPage extends StatefulWidget {
  const LoginPage({super.key});

  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  bool isRegister = false;
  bool isLoading = false;

  final GlobalKey<AFormState> _formKey = GlobalKey<AFormState>();

  Future<String?> submitForm(Map<String, dynamic> value) async {
    setState(() {
      isLoading = true;
    });

    try {
      if (isRegister) {
        await apiAuth.register(
          email: value['email'],
          password: value['password'],
        );
        if (mounted) {
          setState(() {
            isRegister = false;
          });
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Conta criada com sucesso'),
            backgroundColor: DefaultColors.success,
          ),
        );
        }
        return null;
      }

      final LoginResponse result = await apiAuth.login(
        email: value['email'],
        password: value['password'],
      );

      apiBase.setToken(result.accessToken);

      if (mounted) {
        await Navigator.of(context).pushReplacement(
          MaterialPageRoute<dynamic>(
            builder: (_) => const HomePage(),
          ),
        );
      }

      return null;
    } on DioException catch (e) {
      return e.response?.data['detail'] ?? 'Erro ao fazer login';
    } catch (e) {
      return 'Erro ao fazer login';
    } finally {
      if (mounted) {
        setState(() {
          isLoading = false;
        });
      }
    }
  }

  Widget header() {
    return Center(
      child: Text(
        isRegister ? 'Criar conta' : 'Bem vindo', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 24),
      ),
    );
  }

  Widget formAuth() {
    return AForm(
      key: _formKey,
      submitText: isRegister ? 'Criar conta' : 'Entrar',
      showDefaultAction: false,
      fields: <Widget>[
        AFieldEmail(
          identifier: 'email',
        ),
        SizedBox(height: 14),
        AFieldPassword(
          identifier: 'password',
        ),
      ],
      actions: <Widget>[
        Row(
          children: <Widget>[
            AButton(
              text: isRegister ? 'Criar conta' : 'Entrar',
              expanded: true,
              elevation: 0,
              height: 42,
              onPressed: () async {
                final String? result = await submitForm(
                  _formKey.currentState!.getData(),
                );
                if (result != null && mounted) {
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(
                      content: Text(result),
                      backgroundColor: DefaultColors.error,
                    ),
                  );
                }
              },
            ),
          ],
        ),
      ],
      onSubmit: (Object? value) async {
        if (value is Map<String, dynamic>) {
          return submitForm(value);
        }
        return 'Dados inválidos';
      },
    );
  }

  Widget content() {
    return Column(
          children: <Widget>[
            header(),
            formAuth(),
            AButton(
              text: isRegister
            ? 'Já tenho uma conta'
        : 'Não tenho uma conta',
              elevation: 0,
              color: Colors.transparent,
              textColor: DefaultColors.primary,
              onPressed: isLoading
                  ? null
                  : () {
                setState(() {
                  isRegister = !isRegister;
                });
              },
            ),
          ],
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: PageCardLayout(child: content()),
    );
  }
}