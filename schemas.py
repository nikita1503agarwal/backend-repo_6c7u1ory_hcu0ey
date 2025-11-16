"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List

# Example schemas (replace with your own):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Kazify.ai schemas

class Lesson(BaseModel):
    title: str
    summary: Optional[str] = None
    duration_minutes: Optional[int] = Field(default=None, ge=1)

class Course(BaseModel):
    """
    Courses collection schema
    Collection name: "course"
    """
    title: str = Field(..., description="Course title")
    subtitle: Optional[str] = Field(None, description="Short subtitle")
    level: str = Field("Beginner", description="Beginner / Intermediate / Advanced")
    category: str = Field(..., description="e.g., Prompting, Automation, Data, Vision")
    cover_image: Optional[HttpUrl] = Field(None, description="Cover image URL")
    description: Optional[str] = None
    lessons: List[Lesson] = Field(default_factory=list)
    featured: bool = Field(default=False)

class Lead(BaseModel):
    """
    Leads collection schema
    Collection name: "lead"
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    interest: Optional[str] = Field(None, description="What they want to learn")
    source: Optional[str] = Field("website", description="Lead source")

# Add your own schemas here:
# --------------------------------------------------

# Note: The Flames database viewer will automatically:
# 1. Read these schemas from GET /schema endpoint
# 2. Use them for document validation when creating/editing
# 3. Handle all database operations (CRUD) directly
# 4. You don't need to create any database endpoints!
