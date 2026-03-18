from sqlalchemy import String, Float, Integer, DateTime, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime
import enum

class Base(DeclarativeBase):
    pass

class OrgTier(str, enum.Enum):
    FREE = "free"
    PRO = "pro"

class Organization(Base):
    """
    Represents a tenant (company/store) in the system.

    Each organization is an isolated unit in the multi-tenant architecture.
    All data (users, sales, stock, predictions, etc.) is scoped using org_id.

    Attributes:
        id (str): Unique identifier (UUID) for the organization.
        name (str): Name of the organization.
        tier (OrgTier): Subscription tier (FREE or PRO).
        created_at (datetime): Timestamp when the organization was created.

    Relationships:
        users (List[User]): List of users belonging to this organization.
    """
    # YOUR CODE HERE
    __tablename__ = "organizations"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    createdAt: Mapped[datetime] = mapped_column(DateTime,default=datetime.utcnow)
    tier: Mapped[OrgTier] = mapped_column(SAEnum(OrgTier), default=OrgTier.FREE)
      
    users: Mapped[list["User"]] = relationship(back_populates="organization")


class User(Base):
    """
    Represents a user within an organization.

    Users are associated with a single organization and can have roles
    such as 'owner' or 'member'.

    Attributes:
        id (str): Unique identifier (UUID) for the user.
        email (str): Unique email address used for authentication.
        hashed_password (str): Securely hashed password (never plaintext).
        org_id (str): Foreign key referencing the organization.
        role (str): Role of the user ('owner' or 'member').

    Relationships:
        organization (Organization): The organization this user belongs to.
    """
    __tablename__ = "users"
    
    id: Mapped[str] = mapped_column(String(36),primary_key=True)
    email: Mapped[str] = mapped_column(String(255),unique=True,index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    org_id: Mapped[str] = mapped_column(ForeignKey("organizations.id"),index=True)
    role: Mapped[str] = mapped_column(String(50),default="member")
    organization: Mapped["Organization"] = relationship(back_populates="users")
    

class SalesRecord(Base):
    """
    Stores raw sales transaction data.

    This is time-series data used for demand forecasting and analytics.

    Attributes:
        id (int): Auto-incrementing primary key.
        org_id (str): Organization to which the record belongs.
        timestamp (datetime): Time of the sale.
        product_id (str): Identifier for the product sold.
        category (str): Product category.
        quantity (int): Number of units sold.
        unit_price (float): Price per unit.

    Notes:
        Indexed on org_id, timestamp, and product_id for efficient querying.
    """
    
    __tablename__ = "sales"
    
    id:Mapped[str] = mapped_column(Integer,primary_key=True,autoincrement=True)
    org_id:Mapped[str] = mapped_column(ForeignKey("organizations.id"),index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, index=True)
    product_id: Mapped[str] = mapped_column(String(100),index=True)
    category: Mapped[str] = mapped_column(String(100))
    quantity: Mapped[int] = mapped_column(Integer)
    unit_price: Mapped[float] = mapped_column(float)
    
    
class StockLevel(Base):
    """
    Stores estimated stock levels over time.

    This data is typically collected from sensors or inventory systems
    and is used for monitoring and forecasting.

    Attributes:
        id (int): Auto-incrementing primary key.
        org_id (str): Organization to which the record belongs.
        timestamp (datetime): Time of the reading.
        product_id (str): Identifier for the product.
        estimated_stock_pct (float): Estimated stock percentage (0–100).

    Notes:
        Indexed for fast time-series and product-based queries.
    """
    
    id: Mapped[str] = mapped_column(Integer,primary_key=True,autoincrement=True)
    org_id: Mapped[str] = mapped_column(ForeignKey("organizations.id"))
    timestamp: Mapped[datetime] = mapped_column(DateTime, index=True)
    product_id: Mapped[str] = mapped_column(String(100),index=True)
    estimated_stock_pct: Mapped[float] = mapped_column(Float)
    
    
class Temperature(Base):
    """
    Stores temperature readings from storage environments.

    Useful for monitoring conditions for sensitive or perishable goods.

    Attributes:
        id (int): Auto-incrementing primary key.
        org_id (str): Organization to which the reading belongs.
        timestamp (datetime): Time of the reading.
        temperature (float): Temperature value in degrees.

    Notes:
        Indexed on org_id and timestamp for efficient querying.
    """
    __tablename__ = "temperatures"

    id: Mapped[str] = mapped_column(Integer,primary_key=True,autoincrement=True)
    org_id: Mapped[str] = mapped_column(ForeignKey("organizations.id"))
    timestamp: Mapped[datetime] = mapped_column(DateTime, index=True)
    temperature: Mapped[float] = mapped_column(Float)
    
    
class Prediction(Base):
    """
    Stores forecasted inventory predictions generated by ML models.

    Each record represents predicted stock levels for a product
    at a future date along with confidence intervals.

    Attributes:
        id (int): Auto-incrementing primary key.
        org_id (str): Organization for which prediction is made.
        model_version (str): Version of the ML model used.
        product_id (str): Identifier for the product.
        forecast_date (datetime): Date for which prediction is made.
        predicted_stock_pct (float): Predicted stock percentage.
        predicted_quantity (int): Predicted quantity required.
        confidence_lower (float): Lower bound of prediction confidence.
        confidence_upper (float): Upper bound of prediction confidence.
        created_at (datetime): Timestamp when prediction was generated.
    """
    
    __tablename__ = "predictions"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    org_id: Mapped[str] = mapped_column(ForeignKey("organizations.id"), index=True)
    model_version: Mapped[str] = mapped_column(String(100))
    product_id: Mapped[str] = mapped_column(String(100), index=True)
    forecast_date: Mapped[datetime] = mapped_column(DateTime)
    predicted_stock_pct: Mapped[float] = mapped_column(Float)
    predicted_quantity: Mapped[int] = mapped_column(Integer)
    confidence_lower: Mapped[float] = mapped_column(Float)
    confidence_upper: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class TrainingJob(Base):
    """
    Tracks machine learning training jobs.

    Enables monitoring of training progress, debugging failures,
    and storing model performance metrics.

    Attributes:
        id (str): Unique identifier (UUID) for the job.
        org_id (str): Organization running the training job.
        status (str): Current job status 
                      ('pending', 'running', 'completed', 'failed').
        mlflow_run_id (str | None): Optional MLflow run identifier.
        metrics (str | None): Serialized JSON containing model metrics.
        error_message (str | None): Error details if the job fails.
        started_at (datetime): When the job started.
        completed_at (datetime | None): When the job finished.
    """
    
    __tablename__ = "training_jobs"
    
    id:Mapped[str] = mapped_column(String(36),primary_key=True)
    org_id: Mapped[str] = mapped_column(ForeignKey("organizations.id"))
    status: Mapped[str] = mapped_column(String(50)) # pending | running | completed | failed
    mlflow_run_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    metrics: Mapped[str | None] = mapped_column(String(1000), nullable=True)  # JSON string
    error_message: Mapped[str | None] = mapped_column(String(2000), nullable=True)
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)