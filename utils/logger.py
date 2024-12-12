import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

from config import DATA_DIR

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


class UserStatsLogger:
    def __init__(self, stats_file: str = f"{DATA_DIR}/user_stats.json"):
        self.stats_file = Path(stats_file)
        self.stats_file.parent.mkdir(parents=True, exist_ok=True)

        # Create the file if it doesn't exist
        if not self.stats_file.exists():
            self._write_stats(
                {
                    "total_users": 0,
                    "unique_users": [],  # Will store user IDs
                    "actions": {
                        "start_command": 0,
                        "file_downloads": {"mci": 0, "irancell": 0, "rightel": 0},
                        "tutorial_views": 0,
                        "subscription_checks": 0,
                    },
                    "last_updated": datetime.now().isoformat(),
                }
            )

    def log_action(
        self, user_id: int, username: str, action: str, details: Dict[str, Any] = None
    ) -> None:
        """Update statistics for a user action."""
        try:
            stats = self._read_stats()

            # Update total users if this is a new user
            if user_id not in stats["unique_users"]:
                stats["unique_users"].append(user_id)
                stats["total_users"] += 1

            # Update action counts
            if action == "start_command":
                stats["actions"]["start_command"] += 1
            elif action == "file_sent":
                apn_type = details.get("apn_type", "unknown")
                stats["actions"]["file_downloads"][apn_type] = (
                    stats["actions"]["file_downloads"].get(apn_type, 0) + 1
                )
            elif action == "tutorial_sent":
                stats["actions"]["tutorial_views"] += 1
            elif action == "subscription_required":
                stats["actions"]["subscription_checks"] += 1

            # Update timestamp
            stats["last_updated"] = datetime.now().isoformat()

            # Write updated stats
            self._write_stats(stats)

        except Exception as e:
            logger.error(f"Error updating user stats: {e}")

    def get_stats(self) -> Dict:
        """Get the current statistics."""
        try:
            stats = self._read_stats()
            # Convert unique_users to length for privacy
            stats["unique_users"] = len(stats["unique_users"])
            return stats
        except Exception as e:
            logger.error(f"Error reading stats: {e}")
            return {}

    def _read_stats(self) -> Dict:
        """Read statistics from the JSON file."""
        try:
            return json.loads(self.stats_file.read_text())
        except Exception as e:
            logger.error(f"Error reading stats file: {e}")
            return {
                "total_users": 0,
                "unique_users": [],
                "actions": {
                    "start_command": 0,
                    "file_downloads": {"mci": 0, "irancell": 0, "rightel": 0},
                    "tutorial_views": 0,
                    "subscription_checks": 0,
                },
                "last_updated": datetime.now().isoformat(),
            }

    def _write_stats(self, stats: Dict) -> None:
        """Write statistics to the JSON file."""
        try:
            self.stats_file.write_text(json.dumps(stats, indent=2, ensure_ascii=False))
        except Exception as e:
            logger.error(f"Error writing to stats file: {e}")


# Create a global instance
user_logger = UserStatsLogger()
