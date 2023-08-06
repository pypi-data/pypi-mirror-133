""" Config module. """

#  ISC License
#
#  Copyright (c) 2020–2022, Paul Wilhelm, M. Sc. <anfrage@paulwilhelm.de>
#
#  Permission to use, copy, modify, and/or distribute this software for any
#  purpose with or without fee is hereby granted, provided that the above
#  copyright notice and this permission notice appear in all copies.
#
#  THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
#  WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
#  MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
#  ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
#  WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
#  ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
#  OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

from typing import Optional, Dict, Callable, List, Union, Any
import os
import configparser
import numpy as np
from magneticalc.Backend_Types import BACKEND_CUDA
from magneticalc.Debug import Debug
from magneticalc.Field_Types import B_FIELD
from magneticalc.Perspective_Presets import Perspective_Presets
from magneticalc.Version import Version
from magneticalc.Wire_Presets import Wire_Presets


def get_jit_enabled() -> bool:
    """
    Checks if JIT is enabled (or at least not explicitly disabled).

    @return: Boolean
    """
    return (os.environ["NUMBA_DISABLE_JIT"] == "0") if "NUMBA_DISABLE_JIT" in os.environ else True


class Config:
    """ Config class. """

    # Formatting settings
    FloatPrecision = 4
    CoordinatePrecision = 6

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # Default wire preset
    DefaultWirePreset = "Straight Line"

    # Default perspective preset
    DefaultPerspectivePreset = "Isometric"

    # Default configuration
    Default = {
        "version"                                   : Version.String,
        "backend_type"                              : BACKEND_CUDA,
        "auto_calculation"                          : "True",
        "num_cores"                                 : "0",
        "wire_points_base"                          : None,  # Will be set in __init__
        "wire_stretch"                              : "0.1000, 1.0000, 1.0000",
        "wire_slicer_limit"                         : "0.0500",
        "wire_dc"                                   : "1.0000",
        "wire_close_loop"                           : "True",
        "rotational_symmetry_count"                 : "30",
        "rotational_symmetry_radius"                : "1.0000",
        "rotational_symmetry_axis"                  : "2",
        "rotational_symmetry_offset"                : "0",
        "sampling_volume_padding"                   : "1, 1, 1",
        "sampling_volume_override_padding"          : "False",
        "sampling_volume_bounding_box"              : "0.000000, 0.000000, 0.000000; 0.000000, 0.000000, 0.000000",
        "sampling_volume_resolution_exponent"       : "3",
        "sampling_volume_label_resolution_exponent" : "0",
        "field_type"                                : B_FIELD,
        "field_distance_limit"                      : "0.0008",
        "color_metric"                              : "Log Magnitude",
        "alpha_metric"                              : "Magnitude",
        "field_point_scale"                         : "0.0000",
        "field_arrow_head_scale"                    : "0.7500",
        "field_arrow_line_scale"                    : "0.7500",
        "field_boost"                               : "0.0000",
        "display_field_magnitude_labels"            : "True",
        "show_wire_segments"                        : "True",
        "show_wire_points"                          : "True",
        "show_colored_labels"                       : "True",
        "show_gauss"                                : "False",
        "show_coordinate_system"                    : "True",
        "show_perspective_info"                     : "True",
        "dark_background"                           : "True",
        "azimuth"                                   : None,  # Will be set in __init__
        "elevation"                                 : None,  # Will be set in __init__
        "scale_factor"                              : "3.0000",
        "constraint_count"                          : "0"
    }

    def __init__(self) -> None:
        """
        Initializes the configuration.
        """
        Debug(self, ": Init", init=True)

        # Populate defaults
        self.Default["wire_points_base"] = Config.points_to_str(
            Wire_Presets.get_by_id(Config.DefaultWirePreset)["points"]
        )
        default_azimuth = Perspective_Presets.get_by_id(Config.DefaultPerspectivePreset)["azimuth"]
        default_elevation = Perspective_Presets.get_by_id(Config.DefaultPerspectivePreset)["elevation"]
        self.Default["azimuth"] = f"{float(default_azimuth):.{Config.FloatPrecision}f}"
        self.Default["elevation"] = f"{float(default_elevation):.{Config.FloatPrecision}f}"

        self._config = configparser.ConfigParser()  # Will be overwritten by "load()"

        self._synced = False
        self._changed_callback = None

        self._filename: str = ""

    # ------------------------------------------------------------------------------------------------------------------

    def set_changed_callback(self, config_changed_callback: Callable) -> None:
        """
        Sets the callback for any changes to the configuration.

        @param config_changed_callback: Gets called when the filename or the synchronization flag changed
        """
        self._changed_callback = config_changed_callback

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def get_synced(self) -> bool:
        """
        Returns the synchronization state of the current session.
        """
        return self._synced

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def set_filename(self, filename: str) -> None:
        """
        Sets the filename for the current session.

        @param filename: Filename
        """
        self._filename = os.path.join(os.path.dirname(os.path.dirname(__file__)), filename)

        Debug(self, ".set_filename: file://" + self._filename.replace(" ", "%20"))

    def get_filename(self) -> str:
        """
        Gets the filename of the current session.

        @return: Filename
        """
        return self._filename

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def load(self) -> None:
        """
        Loads the configuration from file.

        """
        Debug(self, ".load()")

        self._config = configparser.ConfigParser()

        self._config.read(self._filename)

        self.set_defaults()

        self._synced = True
        if self._changed_callback is not None:
            self._changed_callback()

        if not os.path.isfile(self._filename):
            # Save newly created default file
            self.save()

    def set_defaults(self) -> None:
        """
        Sets the default key-value pairs. Creates empty "User" section if not present.
        """
        self._config["DEFAULT"] = Config.Default

        if "User" not in self._config:
            Debug(self, ".set_defaults(): Creating empty User section")
            self._config["User"] = {}

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def save(self) -> None:
        """
        Saves the configuration to file.
        """
        Debug(self, ".save()")

        with open(self._filename, "w") as file:
            self._config.write(file)

        self._synced = True
        if self._changed_callback is not None:
            self._changed_callback()

    def close(self) -> None:
        """
        Close configuration.
        """
        Debug(self, ".close()")

    # ------------------------------------------------------------------------------------------------------------------

    def remove_key(self, key: str) -> None:
        """
        Removes a key from the configuration.

        @param key: Key
        """
        if not self._config.remove_option("User", key):
            Debug(self, f".remove_key({key}): ERROR: No such key", error=True)

    # ------------------------------------------------------------------------------------------------------------------

    def get_bool(self, key: str) -> bool:
        """
        Gets boolean value, convert from string.

        @param key: Key
        @return: Value
        """
        return self.get_str(key) == "True"

    def get_float(self, key: str) -> float:
        """
        Gets float value, convert from string.

        @param key: Key
        @return: Value
        """
        return float(self.get_str(key))

    def get_int(self, key: str) -> int:
        """
        Gets integer value, convert from string.

        @param key: Key
        @return: Value
        """
        return int(self.get_str(key))

    def get_points(self, key: str) -> List[List[float]]:
        """
        Gets list of 3D points, convert from string.

        @param key: Key
        @return: List of 3D points
        """
        return Config.str_to_points(self.get_str(key))

    def get_point(self, key: str) -> List[float]:
        """
        Gets a single 3D point, convert from string.

        @param key: Key
        @return: Single 3D point
        """
        return Config.str_to_point(self.get_str(key))

    def get_str(self, key: str) -> str:
        """
        Reads a configuration value. Key must be in "Default" section and may be overridden in "User" section.

        @param key: Key
        @return: Value
        """
        value = self._config.get("User", key)
        return value

    # ------------------------------------------------------------------------------------------------------------------

    def set_bool(self, key: str, value: bool) -> None:
        """
        Sets boolean value, convert to string.

        @param key: Key
        @param value: Value
        """
        self.set_str(key, "True" if value else "False")

    def set_float(self, key: str, value: float) -> None:
        """
        Sets float value, convert to string.

        @param key: Key
        @param value: Value
        """
        self.set_str(key, f"{float(value):.{Config.FloatPrecision}f}")

    def set_int(self, key: str, value: int) -> None:
        """
        Sets integer value, convert to string.

        @param key: Key
        @param value: Value
        """
        self.set_str(key, str(int(value)))

    def set_points(self, key: str, value: Union[np.ndarray, List[List[float]]]) -> None:
        """
        Sets list of 3D points, convert to string.

        @param key: Key
        @param value: List of 3D points
        """
        self.set_str(key, Config.points_to_str(value))

    def set_point(self, key: str, value: Union[np.ndarray, List[float]]) -> None:
        """
        Sets a single 3D point, convert to string.

        @param key: Key
        @param value: Single 3D point
        """
        self.set_str(key, Config.point_to_str(value))

    def set_str(self, key: str, value: str) -> None:
        """
        Writes a configuration value. Key must be in "Default" section and may be overridden in "User" section.

        @param key: Key
        @param value: Value
        """
        self._config.set("User", key, value)
        self._synced = False
        if self._changed_callback is not None:
            self._changed_callback()

    def set_get_bool(self, key: str, value: bool) -> bool:
        """
        If value is not None, writes and returns key-value; otherwise (if value is None), reads and returns key-value.

        @param key: Key
        @param value: Value
        """
        if value is None:
            return self.get_bool(key)
        else:
            self.set_bool(key, value)
            return value

    def set_get_float(self, key: str, value: float) -> float:
        """
        If value is not None, writes and returns key-value; otherwise (if value is None), reads and returns key-value.

        @param key: Key
        @param value: Value
        """
        if value is None:
            return self.get_float(key)
        else:
            self.set_float(key, value)
            return value

    def set_get_int(self, key: str, value: int) -> int:
        """
        If value is not None, writes and returns key-value; otherwise (if value is None), reads and returns key-value.

        @param key: Key
        @param value: Value
        """
        if value is None:
            return self.get_int(key)
        else:
            self.set_int(key, value)
            return value

    def set_get_points(
            self,
            key: str,
            value: Union[np.ndarray, List[List[float]]]
    ) -> Union[np.ndarray, List[List[float]]]:
        """
        If value is not None, writes and returns key-value; otherwise (if value is None), reads and returns key-value.

        @param key: Key
        @param value: Value
        """
        if value is None:
            return self.get_points(key)
        else:
            self.set_points(key, value)
            return value

    def set_get_point(
            self,
            key: str,
            value: Union[np.ndarray, List[float]]
    ) -> Union[np.ndarray, List[float]]:
        """
        If value is not None, writes and returns key-value; otherwise (if value is None), reads and returns key-value.

        @param key: Key
        @param value: Value
        """
        if value is None:
            return self.get_point(key)
        else:
            self.set_point(key, value)
            return value

    def set_get_str(self, key: str, value: str) -> str:
        """
        If value is not None, writes and returns key-value; otherwise (if value is None), reads and returns key-value.

        @param key: Key
        @param value: Value
        """
        if value is None:
            return self.get_str(key)
        else:
            self.set_str(key, value)
            return value

    # ------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def point_to_str(point: Union[np.ndarray, List[float]]) -> str:
        """
        Converts a single 3D point to string.

        @param point: Single 3D point
        @return: String
        """
        return \
            f"{point[0]:+0.0{Config.CoordinatePrecision}f}, " \
            f"{point[1]:+0.0{Config.CoordinatePrecision}f}, " \
            f"{point[2]:+0.0{Config.CoordinatePrecision}f}"

    @staticmethod
    def points_to_str(points: Union[np.ndarray, List[List[float]]]) -> str:
        """
        Converts list of 3D points to string.

        @param points: List of 3D points
        @return: String
        """
        return "; ".join([Config.point_to_str(point) for point in points])

    @staticmethod
    def str_to_point(str_point: str) -> Union[np.ndarray, List[float]]:
        """
        Converts string to single 3D point.

        @param str_point: String
        @return: Single 3D point
        """
        return [float(coord) for coord in str_point.split(",")]

    @staticmethod
    def str_to_points(str_points: str) -> Union[np.ndarray, List[List[float]]]:
        """
        Converts string to list of 3D points.

        @param str_points: String
        @return: List of 3D points
        """
        return [
            Config.str_to_point(str_point) for str_point in str_points.split(";")
            if str_point != ""  # Ignoring stray semicolon at the end of the line
        ]

    # ------------------------------------------------------------------------------------------------------------------

    def get_generic(
            self,
            _key: str,
            _type: str
    ) -> Union[bool, float, int, str, np.ndarray, List[float], List[List[float]]]:
        """
        Gets some "_key"-"_value" of data type "_type".

        @param _key: Key
        @param _type: Data type
        @return: Data (type determined by "_type")
        """
        set_func = {
            "bool"  : self.get_bool,
            "float" : self.get_float,
            "int"   : self.get_int,
            "point" : self.get_point,
            "points": self.get_points,
            "str"   : self.get_str
        }

        if _type in set_func:
            return set_func[_type](_key)
        else:
            raise TypeError("Invalid type")

    def set_generic(
            self,
            _key: str,
            _type: str,
            _value: Union[bool, float, int, str, np.ndarray, List[float], List[List[float]]]
    ) -> None:
        """
        Sets some "_key"-"_value" of data type "_type".

        @param _key: Key
        @param _type: Data type
        @param _value: Data (type determined by "_type")
        """
        set_func = {
            "bool"  : self.set_bool,
            "float" : self.set_float,
            "int"   : self.set_int,
            "point" : self.set_point,
            "points": self.set_points,
            "str"   : self.set_str
        }

        if _type in set_func:
            set_func[_type](_key, _value)
        else:
            raise TypeError("Invalid type")

    def set_get_dict(self, prefix: str, suffix: str, types: Dict, values: Optional[Dict]) -> Dict:
        """
        If "values" is None, reads and returns all key-values in "types".
        Note: The actual keys saved in the configuration file are prefixed with "prefix", and suffixed with "suffix".

        If "values" is not None, writes and returns all key-values in "types".
        Note: In this case, "values" must have the same keys as "types".

        @param prefix: Prefix
        @param suffix: Suffix
        @param types: Key:Type (Dictionary)
        @param values: Key:Value (Dictionary)
        """
        if values is None:
            result = {}
            for _key, _type in types.items():
                result[_key] = self.get_generic(prefix + _key + suffix, _type)
            return result
        else:
            for _key, _type in types.items():
                self.set_generic(prefix + _key + suffix, _type, values[_key])
            return values
