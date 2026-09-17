import 'package:flutter/material.dart';

import '../../core/default_colors.dart';

class PageCardLayout extends StatelessWidget {
  final Widget child;
  final Gradient? gradient;
  final Color? backgroundColor;

  const PageCardLayout({
    super.key,
    required this.child,
    this.gradient,
    this.backgroundColor,
  });

  @override
  Widget build(BuildContext context) {
    final bool isDark = Theme.of(context).brightness == Brightness.dark;
    return Container(
      width: double.infinity,
      height: double.infinity,
      decoration: BoxDecoration(
        gradient:
        gradient ??
            (backgroundColor == null
                ? (isDark
                ? DefaultColors.backgroundGradientDark
                : DefaultColors.backgroundGradientLight)
                : null),
        color: backgroundColor,
      ),
      child: Center(
        child: SingleChildScrollView(
          child: Container(
            constraints: const BoxConstraints(maxWidth: 600),
            margin: const EdgeInsets.all(24),
            padding: const EdgeInsets.all(32),
            decoration: BoxDecoration(
              color: Theme.of(context).cardColor,
              borderRadius: BorderRadius.circular(24),
              boxShadow: <BoxShadow>[
                BoxShadow(
                  color: isDark
                      ? Colors.black.withValues(alpha: 0.6)
                      : Colors.black.withValues(alpha: 0.1),
                  blurRadius: 20,
                  offset: const Offset(0, 10),
                ),
              ],
            ),
            child: child,
          ),
        ),
      ),
    );
  }
}