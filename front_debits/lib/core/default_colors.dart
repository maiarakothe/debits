import 'package:flutter/material.dart';

abstract class DefaultColors {
  static const Color primary = Color(0xFF6A00FF);
  static const Color secondary = Color(0xFF4B7BFF);
  static const Color accent = Color(0xFFFF4F9A);

  static const Color text = Color(0xFF2D2D2D);
  static const Color textSecondary = Color(0xFF6B7280);

  static const Color pageColor = Color(0xFFF9FAFF);
  static const Color darkPageColor = Color(0xFF1E1E2E);
  static const Color cardLight = Color(0xFFFFFFFF);
  static const Color cardDark = Color(0xFF2A2A3D);

  static const Color success = Color(0xFF4CAF91);
  static const Color info = Color(0xFF5C7CFF);
  static const Color error = Color(0xFFFF5A5A);
  static const Color warning = Color(0xFFFFB347);

  static const LinearGradient backgroundGradientLight = LinearGradient(
    colors: <Color>[Color(0xFFFFD3E0), Color(0xFFD4E2FF)],
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
  );

  // static const LinearGradient primaryButtonGradient = LinearGradient(
  //   colors: <Color>[Color(0xFF6A00FF), Color(0xFF4B7BFF)],
  // );

  static const LinearGradient backgroundGradientHover = LinearGradient(
    colors: <Color>[Color(0xFFFF5FA2), Color(0xFF7B5CFF)],
  );

  static const LinearGradient backgroundGradient = LinearGradient(
    colors: <Color>[Color(0xFFFF6FB1), Color(0xFF6A8CFF)],
  );

  static const LinearGradient backgroundGradientDark = LinearGradient(
    colors: <Color>[Color(0xFF1E1E2E), Color(0xFF2A2A3D), Color(0xFF3A3A5A)],
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
  );
}

ThemeData themeLightData() {
  return ThemeData(
    brightness: Brightness.light,
    fontFamily: 'Montserrat',
    scaffoldBackgroundColor: DefaultColors.pageColor,
    primaryColor: DefaultColors.primary,
    useMaterial3: false,
    colorScheme: ColorScheme.light(
      primary: DefaultColors.primary,
      secondary: DefaultColors.secondary,
    ),
    appBarTheme: const AppBarTheme(
      elevation: 0,
      backgroundColor: Colors.transparent,
      foregroundColor: DefaultColors.text,
    ),
    elevatedButtonTheme: ElevatedButtonThemeData(
      style: ElevatedButton.styleFrom(
        backgroundColor: DefaultColors.primary,
        foregroundColor: Colors.white,
        elevation: 6,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.all(Radius.circular(12)),
        ),
      ),
    ),
    cardTheme: CardThemeData(
      color: DefaultColors.cardLight,
      elevation: 6,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
    ),
    textTheme: const TextTheme(
      bodyMedium: TextStyle(color: DefaultColors.text, fontSize: 16),
    ),
  );
}

ThemeData themeDarkData() {
  return ThemeData(
    brightness: Brightness.dark,
    fontFamily: 'Montserrat',
    scaffoldBackgroundColor: DefaultColors.darkPageColor,
    primaryColor: DefaultColors.primary,
    useMaterial3: false,
    colorScheme: ColorScheme.dark(
      primary: DefaultColors.primary,
      secondary: DefaultColors.secondary,
    ),
    appBarTheme: const AppBarTheme(
      elevation: 0,
      backgroundColor: Colors.transparent,
      foregroundColor: Colors.white,
    ),
    elevatedButtonTheme: ElevatedButtonThemeData(
      style: ElevatedButton.styleFrom(
        backgroundColor: DefaultColors.primary,
        foregroundColor: Colors.white,
        elevation: 6,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.all(Radius.circular(12)),
        ),
      ),
    ),
    cardTheme: CardThemeData(
      color: DefaultColors.cardDark,
      elevation: 4,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
    ),
    textTheme: const TextTheme(bodyMedium: TextStyle(color: Colors.white)),
  );
}