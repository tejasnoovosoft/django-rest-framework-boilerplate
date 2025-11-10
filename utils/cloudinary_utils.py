import cloudinary.uploader
from typing import Optional
import uuid


def upload_image_to_cloudinary(
    image_file,
    folder: str = "images",
    public_id: Optional[str] = None,
    overwrite: bool = True,
    transformation: Optional[dict] = None,
) -> Optional[str]:
    """
    Upload an image to Cloudinary and return the secure URL.

    Args:
        image_file: The image file to upload
        folder: Cloudinary folder path (default: "images")
        public_id: Custom public ID (default: generates UUID)
        overwrite: Whether to overwrite existing files
        transformation: Optional transformation dict (e.g., {"width": 500, "height": 500, "crop": "fill"})

    Returns:
        Secure URL of uploaded image or None if upload fails
    """
    if not image_file:
        return None

    try:
        # Generate unique ID if not provided
        if not public_id:
            public_id = f"{folder}_{uuid.uuid4().hex}"

        upload_params = {
            "folder": folder,
            "public_id": public_id,
            "overwrite": overwrite,
            "resource_type": "image",
        }

        # Add transformation if provided
        if transformation:
            upload_params["transformation"] = transformation

        upload_result = cloudinary.uploader.upload(image_file, **upload_params)
        return upload_result["secure_url"]

    except Exception as e:
        # Log the error (use proper logging in production)
        print(f"Cloudinary upload failed: {e}")
        return None


def upload_profile_picture(
    image_file, user_identifier: Optional[str] = None
) -> Optional[str]:
    """
    Upload a profile picture to Cloudinary.

    Args:
        image_file: The image file to upload
        user_identifier: Optional user identifier for public_id

    Returns:
        Secure URL of uploaded profile picture
    """
    public_id = f"user_{user_identifier}" if user_identifier else None

    # Add transformation for profile pictures (optional)
    transformation = {
        "width": 400,
        "height": 400,
        "crop": "fill",
        "gravity": "face",
        "quality": "auto",
    }

    return upload_image_to_cloudinary(
        image_file=image_file,
        folder="profile_pictures",
        public_id=public_id,
        transformation=transformation,
    )
