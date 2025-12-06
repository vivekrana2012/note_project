#!/bin/bash
# filepath: /Users/viv/CascadeProjects/note_project/setup_cron.sh

# Get the absolute path of the project directory
PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PYTHON_PATH=$(which python)

# Create logs directory if it doesn't exist
mkdir -p "$PROJECT_DIR/logs"

# Cron job to run every day at 12 PM IST (6:30 AM UTC)
# Note: IST is UTC+5:30, so 12:00 PM IST = 6:30 AM UTC
CRON_SCHEDULE="30 6 * * *"

# Full cron command with caffeinate
CRON_COMMAND="cd $PROJECT_DIR && /usr/bin/caffeinate -dims $PYTHON_PATH startup_script.py >> logs/cron.log 2>&1"

# Display the cron entry
echo "The following cron job will be added:"
echo "$CRON_SCHEDULE $CRON_COMMAND"
echo ""
echo "Schedule: Daily at 12:00 PM IST (6:30 AM UTC)"
echo ""
echo "To add this cron job, run:"
echo "crontab -e"
echo ""
echo "Then add this line:"
echo "$CRON_SCHEDULE $CRON_COMMAND"
echo ""
echo "Note: caffeinate -dims will prevent the system from sleeping during execution"
echo "  -d: prevent display from sleeping"
echo "  -i: prevent system from idle sleeping"
echo "  -m: prevent disk from idle sleeping"
echo "  -s: prevent system from sleeping (AC power only)"