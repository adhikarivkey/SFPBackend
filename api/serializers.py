from rest_framework import serializers


class CostEfficientRouteSerializer(serializers.Serializer):
    start = serializers.CharField(
        max_length=255,
        help_text="Starting address (e.g., '1234 Sunset Blvd, Los Angeles, CA 90026')",
        style={'placeholder': 'Enter start address'}
    )
    end = serializers.CharField(
        max_length=255,
        help_text="Ending address (e.g., '750 7th Ave, New York, NY 10019')",
        style={'placeholder': 'Enter end address'}
    )

    def validate(self, attrs):
        if not attrs.get("start"):
            raise serializers.ValidationError("Start address is required")
        if not attrs.get("end"):
            raise serializers.ValidationError("End address is required")
        return attrs