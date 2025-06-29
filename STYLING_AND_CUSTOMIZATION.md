# Styling & Customization: Clinic Management System

This document describes the styling system, color palette, and how to customize the application's appearance for AI and developer reference.

## Central Styling (styles.py)
- All UI styling is defined in `styles.py`.
- Uses a central color palette for consistency.
- Provides main application stylesheet (`MAIN_STYLE`) and helper functions for message boxes, tables, buttons, and input fields.

## Color Palette
```
COLORS = {
    'primary': '#1e88e5',      # Main blue
    'primary_light': '#64b5f6', # Light blue
    'primary_dark': '#1565c0',  # Dark blue
    'secondary': '#f5f9ff',    # Very light blue for backgrounds
    'accent': '#2196f3',       # Accent blue
    'success': '#4caf50',      # Green for success
    'warning': '#ff9800',      # Orange for warnings
    'error': '#f44336',        # Red for errors
    'text': '#2c3e50',         # Dark blue-gray for text
    'text_light': '#546e7a',   # Light blue-gray for secondary text
    'border': '#e0e0e0',       # Light gray for borders
    'white': '#ffffff',        # White
    'black': '#000000',        # Black
}
```

## Main Stylesheet
- Applies consistent styles to windows, widgets, headers, tabs, buttons, tables, input fields, dialogs, message boxes, forms, status bars, and scroll bars.
- Example: Tabs use the primary color for selection, tables have alternate row colors, and buttons use the primary color with hover/pressed states.

## Customization
- To change the application's appearance, edit the values in the `COLORS` dictionary in `styles.py`.
- To adjust widget or layout styles, modify the corresponding CSS rules in `MAIN_STYLE` or helper functions.
- Custom widgets in `custom_widgets.py` inherit these styles and provide enhanced keyboard navigation.

---

For more details, see `styles.py` and `custom_widgets.py`. 