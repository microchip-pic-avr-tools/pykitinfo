# Changelog

## [1.0.3] - January 2024

### Added
- DSG-5792 added brief mode for reporting serial port only
- DSG-6091 added support for reading out nEDBG extension information
- DSG-6444 added support for PICkit 5

### Fixed
- DSG-5767 fixed unicode output in long mode
- DSG-6310 added fault tolerance for non-numeric interface numbers
- DSG-7084 fixed crash on Mac when virtual serial port is missing serial number
- DSG-7087 added fault tolerance for USB devices missing serial number

## [0.4.0] - November 2022

### Changed
- DSG-5562 added catch-all exception handling in CLI; added return code
- DSG-5624 improved port detection using updated pyedbglib (requirement)
- DSG-5551 removed metadata tag for Python 3.6
- DSG-5450 added metadata tag for Python 3.10

## [0.3.1] - December 2021

### Added
- DSG-3826 PICkit3 support
- DSG-3903 WinUSB tools support
- DSG-4140 Help updates
- DSG-4195 Documentation output

### Fixed
- DSG-3407 Serial port detection on Xplained Pro
- DSG-3409 CLI argument -R
- DSG-3410 Xplained Pro kit name reporting

## [0.1.2] - May 2021
- First public release to PyPi