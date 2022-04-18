# Internal errors
ERR_INTERNAL_ERROR_CODE = 500
ERR_INTERNAL_ERROR_MSG = "Internal error"

# Parameter errors
ERR_MISSING_REQUIRED_FIELD_CODE = 1000
ERR_MISSING_REQUIRED_FIELD_MSG = "Missing required fields"

ERR_VALUE_ERROR_CODE = 1001
ERR_VALUE_ERROR_MSG = "Field value error"

# Business errors
ERR_RESERVATION_CONFLICT_CODE = 2001
ERR_RESERVATION_CONFLICT_MSG = "Conflit with existing reservations"

# Quietness warning code
# Do not change this code unless you make sure you change the warning check in the templates/index.html as well
WARNING_RESERVATION_CONFLICT_CODE = 12000
WARNING_RESERVATION_CONFLICT_MSG = "Warning: New reservation has conflition with existing reservations on quietness option"

# Team list errors
ERR_LACK_OF_AUTHORITY_CODE = 3001
ERR_LACK_OF_AUTHORITY_MSG = "Lack of authority to do this action."

ERR_MISSING_TEAM_NAME_CODE = 3002
ERR_MISSING_TEAM_NAME_MSG = "Missing the team name."

ERR_MISSING_TEAM_LEADER_CODE = 3003
ERR_MISSING_TEAM_LEADER_MSG = "Missing the team leader."

ERR_ADMIN_STAFF_TEAM_LEADER_CODE = 3004
ERR_ADMIN_STAFF_TEAM_LEADER_MSG = "The leader can't be an admin or a staff."

ERR_LEADER_NOT_A_MEMBER_OF_THE_TEAM_CODE = 3005
ERR_LEADER_NOT_A_MEMBER_OF_THE_TEAM_MSG = "The new leader should be a member in the team."

ERR_LEADER_INVALID_CODE = 3006
ERR_LEADER_INVALID_MSG = "The leader id is invalid."

# Team detail errors
ERR_NO_TEAM_ACCESS_CODE = 4001
ERR_NO_TEAM_ACCESS_MSG = "You have no access to the page."

ERR_ADD_INVALID_MEMBER_CODE = 4002
ERR_ADD_INVALID_MEMBER_MSG = "The new added member shouldn't be an admin or a staff."

ERR_NOT_A_MEMBER_OF_THE_TEAM_CODE = 4003
ERR_NOT_A_MEMBER_OF_THE_TEAM_MSG = "Delete a member not in the team."
