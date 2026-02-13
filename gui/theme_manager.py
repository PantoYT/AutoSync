"""
Theme Manager
Handles GUI themes and styling
"""

from typing import Dict, Any


class Theme:
    """Theme color definitions"""
    
    def __init__(self, name: str, colors: Dict[str, str]):
        self.name = name
        self.colors = colors
    
    def get_stylesheet(self) -> str:
        """Generate Qt stylesheet from theme"""
        return f"""
            /* Main Window */
            QMainWindow {{
                background-color: {self.colors['background']};
                color: {self.colors['text']};
            }}
            
            /* Widgets */
            QWidget {{
                background-color: {self.colors['background']};
                color: {self.colors['text']};
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 10pt;
            }}
            
            /* Buttons */
            QPushButton {{
                background-color: {self.colors['button_bg']};
                color: {self.colors['button_text']};
                border: 1px solid {self.colors['border']};
                border-radius: 4px;
                padding: 6px 12px;
                font-weight: bold;
            }}
            
            QPushButton:hover {{
                background-color: {self.colors['button_hover']};
            }}
            
            QPushButton:pressed {{
                background-color: {self.colors['button_pressed']};
            }}
            
            QPushButton:disabled {{
                background-color: {self.colors['disabled']};
                color: {self.colors['text_secondary']};
            }}
            
            /* Primary Button */
            QPushButton#primaryButton {{
                background-color: {self.colors['primary']};
                color: {self.colors['primary_text']};
            }}
            
            QPushButton#primaryButton:hover {{
                background-color: {self.colors['primary_hover']};
            }}
            
            /* Success Button */
            QPushButton#successButton {{
                background-color: {self.colors['success']};
                color: white;
            }}
            
            /* Warning Button */
            QPushButton#warningButton {{
                background-color: {self.colors['warning']};
                color: white;
            }}
            
            /* Danger Button */
            QPushButton#dangerButton {{
                background-color: {self.colors['danger']};
                color: white;
            }}
            
            /* Tables */
            QTableWidget {{
                background-color: {self.colors['widget_bg']};
                alternate-background-color: {self.colors['alternate_bg']};
                gridline-color: {self.colors['border']};
                border: 1px solid {self.colors['border']};
                border-radius: 4px;
            }}
            
            QTableWidget::item {{
                padding: 4px;
            }}
            
            QTableWidget::item:selected {{
                background-color: {self.colors['selection']};
                color: {self.colors['selection_text']};
            }}
            
            QHeaderView::section {{
                background-color: {self.colors['header_bg']};
                color: {self.colors['header_text']};
                padding: 6px;
                border: none;
                border-bottom: 2px solid {self.colors['primary']};
                font-weight: bold;
            }}
            
            /* Text Edit / Log Panel */
            QTextEdit, QPlainTextEdit {{
                background-color: {self.colors['widget_bg']};
                color: {self.colors['text']};
                border: 1px solid {self.colors['border']};
                border-radius: 4px;
                padding: 4px;
                font-family: 'Consolas', 'Courier New', monospace;
            }}
            
            /* Line Edit */
            QLineEdit {{
                background-color: {self.colors['widget_bg']};
                color: {self.colors['text']};
                border: 1px solid {self.colors['border']};
                border-radius: 4px;
                padding: 6px;
            }}
            
            QLineEdit:focus {{
                border: 1px solid {self.colors['primary']};
            }}
            
            /* Combo Box */
            QComboBox {{
                background-color: {self.colors['widget_bg']};
                color: {self.colors['text']};
                border: 1px solid {self.colors['border']};
                border-radius: 4px;
                padding: 6px;
            }}
            
            QComboBox::drop-down {{
                border: none;
            }}
            
            QComboBox QAbstractItemView {{
                background-color: {self.colors['widget_bg']};
                color: {self.colors['text']};
                selection-background-color: {self.colors['selection']};
            }}
            
            /* Progress Bar */
            QProgressBar {{
                background-color: {self.colors['widget_bg']};
                border: 1px solid {self.colors['border']};
                border-radius: 4px;
                text-align: center;
                color: {self.colors['text']};
            }}
            
            QProgressBar::chunk {{
                background-color: {self.colors['primary']};
                border-radius: 3px;
            }}
            
            /* Status Bar */
            QStatusBar {{
                background-color: {self.colors['status_bg']};
                color: {self.colors['text']};
                border-top: 1px solid {self.colors['border']};
            }}
            
            /* Menu Bar */
            QMenuBar {{
                background-color: {self.colors['menu_bg']};
                color: {self.colors['text']};
                border-bottom: 1px solid {self.colors['border']};
            }}
            
            QMenuBar::item:selected {{
                background-color: {self.colors['primary']};
            }}
            
            QMenu {{
                background-color: {self.colors['menu_bg']};
                color: {self.colors['text']};
                border: 1px solid {self.colors['border']};
            }}
            
            QMenu::item:selected {{
                background-color: {self.colors['selection']};
            }}
            
            /* Scroll Bar */
            QScrollBar:vertical {{
                background-color: {self.colors['widget_bg']};
                width: 12px;
                border-radius: 6px;
            }}
            
            QScrollBar::handle:vertical {{
                background-color: {self.colors['scroll_handle']};
                border-radius: 6px;
                min-height: 20px;
            }}
            
            QScrollBar::handle:vertical:hover {{
                background-color: {self.colors['scroll_handle_hover']};
            }}
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
            
            /* Tab Widget */
            QTabWidget::pane {{
                border: 1px solid {self.colors['border']};
                border-radius: 4px;
            }}
            
            QTabBar::tab {{
                background-color: {self.colors['tab_bg']};
                color: {self.colors['text_secondary']};
                padding: 8px 16px;
                border: 1px solid {self.colors['border']};
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }}
            
            QTabBar::tab:selected {{
                background-color: {self.colors['tab_selected']};
                color: {self.colors['text']};
                border-bottom: 2px solid {self.colors['primary']};
            }}
            
            /* Splitter */
            QSplitter::handle {{
                background-color: {self.colors['border']};
            }}
            
            QSplitter::handle:hover {{
                background-color: {self.colors['primary']};
            }}
        """


class ThemeManager:
    """Manage application themes"""
    
    THEMES = {
        'dark-blue-yellow': Theme('Dark Blue & Yellow', {
            'background': '#1e1e2e',
            'widget_bg': '#2a2a3e',
            'alternate_bg': '#252535',
            'text': '#e0e0e0',
            'text_secondary': '#a0a0a0',
            'primary': '#ffd700',
            'primary_hover': '#ffed4e',
            'primary_text': '#1e1e2e',
            'button_bg': '#3a3a4e',
            'button_hover': '#4a4a5e',
            'button_pressed': '#2a2a3e',
            'button_text': '#e0e0e0',
            'success': '#4caf50',
            'warning': '#ff9800',
            'danger': '#f44336',
            'border': '#3a3a4e',
            'selection': '#ffd700',
            'selection_text': '#1e1e2e',
            'header_bg': '#2a2a3e',
            'header_text': '#ffd700',
            'status_bg': '#252535',
            'menu_bg': '#2a2a3e',
            'tab_bg': '#2a2a3e',
            'tab_selected': '#3a3a4e',
            'scroll_handle': '#5a5a6e',
            'scroll_handle_hover': '#6a6a7e',
            'disabled': '#3a3a3e'
        }),
        
        'black-white': Theme('Black & White', {
            'background': '#000000',
            'widget_bg': '#1a1a1a',
            'alternate_bg': '#0f0f0f',
            'text': '#ffffff',
            'text_secondary': '#aaaaaa',
            'primary': '#ffffff',
            'primary_hover': '#e0e0e0',
            'primary_text': '#000000',
            'button_bg': '#2a2a2a',
            'button_hover': '#3a3a3a',
            'button_pressed': '#1a1a1a',
            'button_text': '#ffffff',
            'success': '#4caf50',
            'warning': '#ff9800',
            'danger': '#f44336',
            'border': '#2a2a2a',
            'selection': '#ffffff',
            'selection_text': '#000000',
            'header_bg': '#1a1a1a',
            'header_text': '#ffffff',
            'status_bg': '#0f0f0f',
            'menu_bg': '#1a1a1a',
            'tab_bg': '#1a1a1a',
            'tab_selected': '#2a2a2a',
            'scroll_handle': '#4a4a4a',
            'scroll_handle_hover': '#5a5a5a',
            'disabled': '#2a2a2a'
        }),
        
        'system': Theme('System Default', {
            # Minimal styling to use system defaults
            'background': 'palette(window)',
            'widget_bg': 'palette(base)',
            'alternate_bg': 'palette(alternate-base)',
            'text': 'palette(window-text)',
            'text_secondary': 'palette(mid)',
            'primary': 'palette(highlight)',
            'primary_hover': 'palette(highlight)',
            'primary_text': 'palette(highlighted-text)',
            'button_bg': 'palette(button)',
            'button_hover': 'palette(light)',
            'button_pressed': 'palette(dark)',
            'button_text': 'palette(button-text)',
            'success': '#4caf50',
            'warning': '#ff9800',
            'danger': '#f44336',
            'border': 'palette(mid)',
            'selection': 'palette(highlight)',
            'selection_text': 'palette(highlighted-text)',
            'header_bg': 'palette(button)',
            'header_text': 'palette(button-text)',
            'status_bg': 'palette(window)',
            'menu_bg': 'palette(window)',
            'tab_bg': 'palette(button)',
            'tab_selected': 'palette(base)',
            'scroll_handle': 'palette(mid)',
            'scroll_handle_hover': 'palette(midlight)',
            'disabled': 'palette(mid)'
        })
    }
    
    def __init__(self):
        self.current_theme_name = 'dark-blue-yellow'
    
    def get_theme(self, theme_name: str = None) -> Theme:
        """Get theme by name"""
        if theme_name is None:
            theme_name = self.current_theme_name
        
        return self.THEMES.get(theme_name, self.THEMES['dark-blue-yellow'])
    
    def set_theme(self, theme_name: str):
        """Set current theme"""
        if theme_name in self.THEMES:
            self.current_theme_name = theme_name
    
    def get_available_themes(self) -> list:
        """Get list of available theme names"""
        return list(self.THEMES.keys())
    
    def get_stylesheet(self, theme_name: str = None) -> str:
        """Get stylesheet for theme"""
        theme = self.get_theme(theme_name)
        return theme.get_stylesheet()


# Global theme manager
_theme_manager: Theme = None


def get_theme_manager() -> ThemeManager:
    """Get or create global theme manager"""
    global _theme_manager
    if _theme_manager is None:
        _theme_manager = ThemeManager()
    return _theme_manager
