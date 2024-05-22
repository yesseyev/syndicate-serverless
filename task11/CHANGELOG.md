# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - yyyy-MM-dd
### Added
    -  Added items

### Changed
    -  Changed items 

### Removed
    -  Removed items 
syndicate generate meta "cognito_user_pool" \
    --resource_name "simple-booking-userpool" \
    --auto_verified_attributes "email" \
    --username_attributes "email" \
    --custom_attributes firstName String \
    --custom_attributes lastName String 