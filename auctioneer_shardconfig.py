"""
Auctioneer Shard Configuration
Centralized configuration management with environment variable validation.
"""
import os
import logging
from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from datetime import timedelta
import dotenv

# Load environment variables
dotenv.load_dotenv()

@dataclass
class FirebaseConfig:
    """Firebase configuration with validation"""
    project_id: str = field(default_factory=lambda: os.getenv("FIREBASE_PROJECT_ID", ""))
    credentials_path: str = field(default_factory=lambda: os.getenv("GOOGLE_APPLICATION_CREDENTIALS", ""))
    collection_prefix: str = "auctioneer_shard"
    
    def validate(self) -> bool:
        """Validate Firebase configuration"""
        if not self.project_id:
            logging.error("FIREBASE_PROJECT_ID not set")
            return False
        if not os.path.exists(self.credentials_path):
            logging.error(f"Firebase credentials not found at {self.credentials_path}")
            return False
        return True

@dataclass
class MarketConfig:
    """Marketplace configuration"""
    ocean_protocol_enabled: bool = field(
        default_factory=lambda: os.getenv("OCEAN_PROTOCOL_ENABLED", "false").lower() == "true"
    )
    private_api_enabled: bool = field(
        default_factory=lambda: os.getenv("PRIVATE_API_ENABLED", "false").lower() == "true"
    )
    base_price_usd: float = 49.99  # Base price per data packet
    revenue_treasury_address: str = field(
        default_factory=lambda: os.getenv("INFRA_TREASURY_ADDRESS", "")
    )
    min_packet_size_mb: int = 10  # Minimum data size for listing

@dataclass
class TelemetryConfig:
    """Telemetry streaming configuration"""
    sampling_interval_seconds: int = 30  # How often to capture state
    retention_hours: int = 168  # Keep raw data for 7 days
    sanitization_enabled: bool = True  # Remove sensitive identifiers
    max_packet