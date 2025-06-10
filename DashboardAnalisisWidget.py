import sys
import json
import pandas as pd
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea,
    QGroupBox, QTableWidget, QTableWidgetItem, QMessageBox, QApplication,
    QHeaderView, QSizePolicy
)
from PyQt5.QtCore import Qt

from Análisis_Efectividad_Overround import analizar_favorito_odds_vs_overround, cargar_partidos as cargar_pronosticos_overround
from analisis_resumen_global import analizar_efectividad_resumen_global_v2, cargar_pronosticos as cargar_pronosticos_resumen
from analisis_killer_instinct import analizar_killer_instinct_effectiveness, cargar_pronosticos as cargar_pronosticos_ki
from analisis_torneos_efectividad import analizar_torneos_effectiveness, cargar_pronosticos as cargar_pronosticos_torneos
from analisis_oponentes import analizar_rivalidad_effectiveness, cargar_pronosticos as cargar_pronosticos_oponentes

from db_manager import guardar_resultados_analisis_efectividad, DB_NAME, cargar_pronosticos

from PyQt5.QtGui import QClipboard

class DashboardAnalisisWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Dashboard de Análisis de Efectividad")
        self.main_layout = QVBoxLayout(self)

        # --- Contenedor de Botones ---
        button_layout = QHBoxLayout()
        self.btn_actualizar_analisis = QPushButton("🔄 Actualizar Análisis")
        self.btn_actualizar_analisis.clicked.connect(self.ejecutar_todos_los_analisis)
        button_layout.addWidget(self.btn_actualizar_analisis)

        self.btn_guardar_analisis = QPushButton("💾 Guardar Análisis Actual")
        self.btn_guardar_analisis.clicked.connect(self.guardar_analisis_actual)
        self.btn_guardar_analisis.setEnabled(False)
        button_layout.addWidget(self.btn_guardar_analisis)

        # --- Botón para copiar ---
        self.btn_copiar_analisis = QPushButton("📋 Copiar Datos Generados")
        self.btn_copiar_analisis.clicked.connect(self.copiar_datos_analisis)
        self.btn_copiar_analisis.setEnabled(False)
        button_layout.addWidget(self.btn_copiar_analisis)

        self.main_layout.addLayout(button_layout)

        # --- Scroll Area para las Fichas de Análisis ---
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content_widget = QWidget()
        self.fichas_layout = QVBoxLayout(self.scroll_content_widget)
        self.fichas_layout.setAlignment(Qt.AlignTop)
        self.scroll_area.setWidget(self.scroll_content_widget)
        self.main_layout.addWidget(self.scroll_area)

        self.analysis_dataframes = {}
        self.pronosticos_generales_count = 0

        self.modulos_config = [
            {'key': 'overround', 'title': 'Análisis Efectividad Overround', 'func': analizar_favorito_odds_vs_overround, 'params': {'overround_step': 0.05}},
            {'key': 'resumen_global', 'title': 'Análisis Efectividad Resumen Global', 'func': analizar_efectividad_resumen_global_v2, 'params': {}},
            {'key': 'killer_instinct', 'title': 'Análisis Efectividad Killer Instinct', 'func': analizar_killer_instinct_effectiveness, 'params': {}},
            {'key': 'torneos', 'title': 'Análisis Efectividad Torneos', 'func': analizar_torneos_effectiveness, 'params': {}},
            {'key': 'oponentes', 'title': 'Análisis Efectividad Oponentes (Riv/H2H)', 'func': analizar_rivalidad_effectiveness, 'params': {}}
        ]

        self._inicializar_fichas_vacias()

    def _inicializar_fichas_vacias(self):
        for config in self.modulos_config:
            group_box = QGroupBox(config['title'])
            layout_group = QVBoxLayout()
            table_widget = QTableWidget()
            table_widget.setAlternatingRowColors(True)
            table_widget.setEditTriggers(QTableWidget.NoEditTriggers)
            table_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            table_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            table_widget.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
            table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            layout_group.addWidget(table_widget)
            group_box.setLayout(layout_group)
            self.fichas_layout.addWidget(group_box)
            setattr(self, f"table_{config['key']}", table_widget)
            setattr(self, f"group_{config['key']}", group_box)

    def _mostrar_df_en_tabla(self, table_widget, df):
        if df is None or df.empty:
            table_widget.setRowCount(0)
            table_widget.setColumnCount(0)
            table_widget.setMinimumHeight(50)
            table_widget.updateGeometry()
            return

        table_widget.setRowCount(df.shape[0])
        table_widget.setColumnCount(df.shape[1])
        table_widget.setHorizontalHeaderLabels(df.columns)

        for i in range(df.shape[0]):
            for j in range(df.shape[1]):
                item_data = str(df.iloc[i, j])
                item = QTableWidgetItem(item_data)
                table_widget.setItem(i, j, item)
        
        table_widget.resizeColumnsToContents()
        table_widget.resizeRowsToContents()
        height = table_widget.horizontalHeader().height()
        for i in range(df.shape[0]):
            height += table_widget.rowHeight(i)
        height += 5 
        table_widget.setMinimumHeight(height)
        table_widget.setMaximumHeight(height + 10)
        table_widget.updateGeometry()

    def ejecutar_todos_los_analisis(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.btn_guardar_analisis.setEnabled(False)
        self.btn_copiar_analisis.setEnabled(False)
        self.analysis_dataframes = {}

        try:
            pronosticos_db = cargar_pronosticos(DB_NAME)
            self.pronosticos_generales_count = len(pronosticos_db) if pronosticos_db else 0

            for config in self.modulos_config:
                df_analisis = None
                try:
                    df_analisis = config['func'](db_path=DB_NAME, **config['params'])
                    self.analysis_dataframes[config['key']] = df_analisis
                    table_widget = getattr(self, f"table_{config['key']}")
                    self._mostrar_df_en_tabla(table_widget, df_analisis)
                except Exception as e:
                    QMessageBox.warning(self, "Error de Análisis", f"No se pudo completar el análisis '{config['title']}':\n{str(e)}")
                    self.analysis_dataframes[config['key']] = pd.DataFrame()
                    table_widget = getattr(self, f"table_{config['key']}")
                    self._mostrar_df_en_tabla(table_widget, pd.DataFrame())
            self.scroll_content_widget.adjustSize()

            if any(df is not None and not df.empty for df in self.analysis_dataframes.values()):
                self.btn_guardar_analisis.setEnabled(True)
                self.btn_copiar_analisis.setEnabled(True)
            else:
                QMessageBox.information(self, "Análisis Vacío", "Todos los análisis resultaron en datos vacíos. No se puede guardar ni copiar.")

        except Exception as e:
            QMessageBox.critical(self, "Error General", f"Ocurrió un error al ejecutar los análisis: {e}")
        finally:
            QApplication.restoreOverrideCursor()

    def guardar_analisis_actual(self):
        if not self.analysis_dataframes or not self.btn_guardar_analisis.isEnabled():
            QMessageBox.warning(self, "Sin Datos", "No hay datos de análisis para guardar o los datos están vacíos.")
            return

        reply = QMessageBox.question(self, "Confirmar Guardado",
                                     "¿Deseas guardar los resultados del análisis actual en la base de datos?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                guardar_resultados_analisis_efectividad(
                    db_path=DB_NAME,
                    pronosticos_count=self.pronosticos_generales_count,
                    overround_df=self.analysis_dataframes.get('overround'),
                    resumen_df=self.analysis_dataframes.get('resumen_global'),
                    ki_df=self.analysis_dataframes.get('killer_instinct'),
                    torneos_df=self.analysis_dataframes.get('torneos'),
                    oponentes_df=self.analysis_dataframes.get('oponentes')
                )
                QMessageBox.information(self, "Éxito", "Los resultados del análisis han sido guardados.")
            except Exception as e:
                QMessageBox.critical(self, "Error al Guardar", f"No se pudieron guardar los resultados: {e}")

    def copiar_datos_analisis(self):
        if not self.analysis_dataframes or not self.btn_copiar_analisis.isEnabled():
            QMessageBox.warning(self, "Sin Datos", "No hay datos de análisis para copiar o los datos están vacíos.")
            return

        # Construir el texto a copiar
        texto_copiar = ""
        for config in self.modulos_config:
            df = self.analysis_dataframes.get(config['key'])
            if df is not None and not df.empty:
                texto_copiar += f"{config['title']}\n"
                # Usar tabulación para que sea fácil de pegar en Excel
                texto_copiar += df.to_csv(index=False, sep='\t')
                texto_copiar += "\n\n"
        if not texto_copiar.strip():
            QMessageBox.warning(self, "Sin Datos", "No hay datos válidos para copiar.")
            return

        clipboard = QApplication.clipboard()
        clipboard.setText(texto_copiar)
        QMessageBox.information(self, "Copiado", "¡Todos los datos generados han sido copiados al portapapeles!\n\nPuedes pegarlos directamente en un archivo de texto o en Excel.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    from db_manager import init_db 
    init_db()
    main_window = QWidget()
    main_window.setWindowTitle("Panel Principal de Análisis")
    main_window.setGeometry(50, 50, 1000, 700)
    layout = QVBoxLayout(main_window)
    dashboard = DashboardAnalisisWidget()
    layout.addWidget(dashboard)
    main_window.show()
    sys.exit(app.exec_())