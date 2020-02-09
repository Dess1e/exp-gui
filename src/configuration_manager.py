import json
from copy import copy
from typing import List, NamedTuple

from PyQt5.QtWidgets import (
    QWidget, QGridLayout, QFileDialog, QLabel, QLineEdit, QPushButton, QCheckBox,
    QListWidget, QListWidgetItem, QMessageBox
)
from PyQt5.QtGui import QIntValidator, QIcon

from logger import Logger
from utils import filter_numerical_string, pairwise


class ExperimentStage(NamedTuple):
    start_temp: int
    end_temp: int
    stage_duration: int
    is_measurement: bool

    def to_dict(self) -> dict:
        return dict(self._asdict())

    @staticmethod
    def from_dict(dict_: dict):
        return ExperimentStage(
            start_temp=dict_['start_temp'],
            end_temp=dict_['end_temp'],
            stage_duration=dict_['stage_duration'],
            is_measurement=dict_['is_measurement'],
        )


class ConfigurationManager(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle('Create experiment configuration')

        self.layout: QGridLayout = QGridLayout(self)
        self.main_label = QLabel('Fill configuration specs')
        self.heat_from_label = QLabel('Start temperature: ')
        self.heat_to_label = QLabel('Final temperature: ')
        self.stage_duration_label = QLabel('Stage duration: ')
        self.save_button = QPushButton('Save config')
        self.add_button = QPushButton('Add new stage')
        self.delete_button = QPushButton('Delete selected stage')

        int_checker = QIntValidator(1, 9999)

        self.heat_from = QLineEdit()
        self.heat_to = QLineEdit()
        self.stage_duration = QLineEdit()
        self.is_measurement = QCheckBox('Is measurement?')

        self.heat_from.setDisabled(True)
        self.heat_to.setDisabled(True)
        self.stage_duration.setDisabled(True)
        self.is_measurement.setDisabled(True)

        self.heat_from.setValidator(int_checker)
        self.heat_to.setValidator(int_checker)
        self.stage_duration.setValidator(int_checker)

        self.heat_from.setInputMask('000\°\C')
        self.heat_to.setInputMask('000\°\C')
        self.stage_duration.setInputMask('0000\ \s\e\c\o\\n\d\s')

        self.heat_from.setText('0')
        self.heat_to.setText('0')
        self.stage_duration.setText('0')

        self.stages_list_widget = QListWidget(self)

        self.layout.addWidget(self.main_label, 0, 0, 1, 2)
        self.layout.addWidget(self.heat_from_label, 1, 0)
        self.layout.addWidget(self.heat_from, 1, 1)
        self.layout.addWidget(self.heat_to_label, 2, 0)
        self.layout.addWidget(self.heat_to, 2, 1)
        self.layout.addWidget(self.stage_duration_label, 3, 0)
        self.layout.addWidget(self.stage_duration, 3, 1)
        self.layout.addWidget(self.is_measurement, 4, 0, 1, 2)
        self.layout.addWidget(self.add_button, 5, 0, 1, 2)
        self.layout.addWidget(self.delete_button, 6, 0, 1, 2)
        self.layout.addWidget(self.save_button, 7, 0, 1, 2)
        self.layout.addWidget(self.stages_list_widget, 0, 2, 8, 2)

        self.is_measurement.pressed.connect(self.is_measurement_checked)
        self.is_measurement.stateChanged.connect(self.update_stage)
        self.add_button.pressed.connect(self.add_stage)
        self.save_button.pressed.connect(self.save_config)
        self.delete_button.pressed.connect(self.remove_stage)
        self.stages_list_widget.pressed.connect(self.list_press)
        self.heat_to.textChanged.connect(self.update_stage)
        self.heat_from.textChanged.connect(self.update_stage)
        self.stage_duration.textChanged.connect(self.update_stage)

        self.setFixedHeight(300)
        self.setFixedWidth(600)

    def get_values(self):
        return ExperimentStage(
            start_temp=int(filter_numerical_string(self.heat_from.text())),
            end_temp=int(filter_numerical_string(self.heat_to.text())),
            stage_duration=int(filter_numerical_string(self.stage_duration.text())),
            is_measurement=self.is_measurement.isChecked()
        )

    def is_measurement_checked(self):
        if not self.is_measurement.isChecked():
            self.heat_from.setDisabled(True)
            self.heat_to.setDisabled(True)
            self.stage_duration.setDisabled(True)
        else:
            self.heat_from.setDisabled(False)
            self.heat_to.setDisabled(False)
            self.stage_duration.setDisabled(False)

    def remove_stage(self):
        self.stages_list_widget.takeItem(
            self.stages_list_widget.currentRow()
        )
        cnt = self.stages_list_widget.count()
        if cnt != 0:
            self.stages_list_widget.setCurrentItem(
                self.stages_list_widget.item(cnt - 1)
            )
            self.list_press()
        else:
            self.set_input_enabled(False)
            self.is_measurement.setEnabled(False)

    def add_stage(self):
        new_item = StageListItem()
        self.stages_list_widget.addItem(
            new_item
        )
        self.stages_list_widget.setCurrentItem(new_item)
        self.list_press()
        self.stages_list_widget.update()

    def set_input_enabled(self, val: bool):
        self.heat_from.setEnabled(val)
        self.heat_to.setEnabled(val)
        self.stage_duration.setEnabled(val)

    def list_press(self):
        self.set_input_enabled(True)
        self.is_measurement.setEnabled(True)

        selected_list_item, *_ = self.stages_list_widget.selectedItems()
        stage: ExperimentStage = selected_list_item.stage
        self.heat_to.setText(str(stage.end_temp))
        self.heat_from.setText(str(stage.start_temp))
        self.stage_duration.setText(str(stage.stage_duration))
        self.is_measurement.setChecked(stage.is_measurement)

        if self.is_measurement.isChecked():
            self.set_input_enabled(False)

    def update_stage(self):
        selected_list_item, *_ = self.stages_list_widget.selectedItems()
        try:
            stage = ExperimentStage(
                stage_duration=int(filter_numerical_string(self.stage_duration.text())),
                start_temp=int(filter_numerical_string(self.heat_from.text())),
                end_temp=int(filter_numerical_string(self.heat_to.text())),
                is_measurement=self.is_measurement.isChecked()
            )
        except ValueError:
            return
        else:
            selected_list_item.set_data(stage)

    def check_config(self):
        def fire_message(message):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle('Configuration check failed')
            msg.setText(message)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

        items = [
                self.stages_list_widget.item(row).stage
                for row in range(self.stages_list_widget.count())
        ]
        filtered_items = list(filter(lambda s: not s.is_measurement, items))
        for item1, item2 in pairwise(filtered_items):
            if item1.end_temp != item2.start_temp:
                item1_index = items.index(item1) + 1
                item2_index = items.index(item2) + 1
                fire_message(
                    f'Could not validate configuration!\n\n'
                    f'Start temperature of stage {item2_index} and final '
                    f'temperature of stage {item1_index} do not match!'
                    f'\n(Got {item2.start_temp}, {item1.end_temp} expected)'
                )
                return False
            elif item1.stage_duration < 1:
                index = items.index(item1)
                fire_message(f'Stage {index} duration is invalid! Should be greater '
                             f'than 1 but got {item1.stage_duration}')
                return False
            elif item2.stage_duration < 1:
                index = items.index(item2)
                fire_message(f'Stage {index} duration is invalid! Should be greater '
                             f'than 1 but got {item2.stage_duration}')
                return False

        else:
            return True

    # noinspection PyTypeChecker
    def serialize_config(self):
        items: List[StageListItem] = [
            self.stages_list_widget.item(row) for row in range(self.stages_list_widget.count())
        ]
        items_dicts = [item.stage.to_dict() for item in items]
        return json.dumps(items_dicts)

    def deserialize_config(self, raw_data):
        json_data = json.loads(raw_data)
        deserialized_stages = [ExperimentStage.from_dict(raw_stage) for raw_stage in json_data]
        for stage in deserialized_stages:
            new_item = StageListItem()
            new_item.set_data(stage)
            self.stages_list_widget.addItem(
                new_item
            )
        self.stages_list_widget.update()
        self.show()


    def save_config(self):
        config_valid = self.check_config()
        if config_valid:
            serialized_config = self.serialize_config()
            fname, _ = QFileDialog().getSaveFileName(
                self,
                'Select where to save config',
                '.',
                '*.json'
            )
            Logger.log(f'Save config dialog got filename {fname}')
            with open(fname, 'w') as f:
                f.write(serialized_config)
            Logger.log(f'Successfully saved config to file {fname}')

    def load_config(self):
        fname, _ = QFileDialog().getOpenFileName(
            self,
            'Open configuration file',
            '.',
            '*.json'
        )
        Logger.log(f'Load config dialog got filename {fname}')
        if fname:
            with open(fname, 'r') as f:
                data = f.read()
            self.deserialize_config(data)


class StageListItem(QListWidgetItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setText('Empty stage')
        self.stage = ExperimentStage(0, 0, 0, False)

    def set_data(self, stage: ExperimentStage):
        self.stage = stage
        if stage.is_measurement:
            ico = 'measurement'
        elif stage.start_temp > stage.end_temp:
            ico = 'cold'
        else:
            ico = 'heat'
        self.setIcon(QIcon(f'resources/{ico}.ico'))
        if stage.is_measurement:
            self.setText('Measure')
        else:
            self.setText(f'{stage.start_temp}°C -> {stage.end_temp}°C (in {stage.stage_duration} seconds)')