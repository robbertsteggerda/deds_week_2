USE [master]
GO
/****** Object:  Database [greatoutdoors]    Script Date: 5-4-2024 00:18:13 ******/
CREATE DATABASE [greatoutdoors]
 CONTAINMENT = NONE
 ON  PRIMARY 
( NAME = N'greatoutdoors', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL16.SQLEXPRESS\MSSQL\DATA\greatoutdoors.mdf' , SIZE = 73728KB , MAXSIZE = UNLIMITED, FILEGROWTH = 65536KB )
 LOG ON 
( NAME = N'greatoutdoors_log', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL16.SQLEXPRESS\MSSQL\DATA\greatoutdoors_log.ldf' , SIZE = 139264KB , MAXSIZE = 2048GB , FILEGROWTH = 65536KB )
 WITH CATALOG_COLLATION = DATABASE_DEFAULT, LEDGER = OFF
GO
ALTER DATABASE [greatoutdoors] SET COMPATIBILITY_LEVEL = 160
GO
IF (1 = FULLTEXTSERVICEPROPERTY('IsFullTextInstalled'))
begin
EXEC [greatoutdoors].[dbo].[sp_fulltext_database] @action = 'enable'
end
GO
ALTER DATABASE [greatoutdoors] SET ANSI_NULL_DEFAULT OFF 
GO
ALTER DATABASE [greatoutdoors] SET ANSI_NULLS OFF 
GO
ALTER DATABASE [greatoutdoors] SET ANSI_PADDING OFF 
GO
ALTER DATABASE [greatoutdoors] SET ANSI_WARNINGS OFF 
GO
ALTER DATABASE [greatoutdoors] SET ARITHABORT OFF 
GO
ALTER DATABASE [greatoutdoors] SET AUTO_CLOSE OFF 
GO
ALTER DATABASE [greatoutdoors] SET AUTO_SHRINK OFF 
GO
ALTER DATABASE [greatoutdoors] SET AUTO_UPDATE_STATISTICS ON 
GO
ALTER DATABASE [greatoutdoors] SET CURSOR_CLOSE_ON_COMMIT OFF 
GO
ALTER DATABASE [greatoutdoors] SET CURSOR_DEFAULT  GLOBAL 
GO
ALTER DATABASE [greatoutdoors] SET CONCAT_NULL_YIELDS_NULL OFF 
GO
ALTER DATABASE [greatoutdoors] SET NUMERIC_ROUNDABORT OFF 
GO
ALTER DATABASE [greatoutdoors] SET QUOTED_IDENTIFIER OFF 
GO
ALTER DATABASE [greatoutdoors] SET RECURSIVE_TRIGGERS OFF 
GO
ALTER DATABASE [greatoutdoors] SET  DISABLE_BROKER 
GO
ALTER DATABASE [greatoutdoors] SET AUTO_UPDATE_STATISTICS_ASYNC OFF 
GO
ALTER DATABASE [greatoutdoors] SET DATE_CORRELATION_OPTIMIZATION OFF 
GO
ALTER DATABASE [greatoutdoors] SET TRUSTWORTHY OFF 
GO
ALTER DATABASE [greatoutdoors] SET ALLOW_SNAPSHOT_ISOLATION OFF 
GO
ALTER DATABASE [greatoutdoors] SET PARAMETERIZATION SIMPLE 
GO
ALTER DATABASE [greatoutdoors] SET READ_COMMITTED_SNAPSHOT OFF 
GO
ALTER DATABASE [greatoutdoors] SET HONOR_BROKER_PRIORITY OFF 
GO
ALTER DATABASE [greatoutdoors] SET RECOVERY SIMPLE 
GO
ALTER DATABASE [greatoutdoors] SET  MULTI_USER 
GO
ALTER DATABASE [greatoutdoors] SET PAGE_VERIFY CHECKSUM  
GO
ALTER DATABASE [greatoutdoors] SET DB_CHAINING OFF 
GO
ALTER DATABASE [greatoutdoors] SET FILESTREAM( NON_TRANSACTED_ACCESS = OFF ) 
GO
ALTER DATABASE [greatoutdoors] SET TARGET_RECOVERY_TIME = 60 SECONDS 
GO
ALTER DATABASE [greatoutdoors] SET DELAYED_DURABILITY = DISABLED 
GO
ALTER DATABASE [greatoutdoors] SET ACCELERATED_DATABASE_RECOVERY = OFF  
GO
ALTER DATABASE [greatoutdoors] SET QUERY_STORE = ON
GO
ALTER DATABASE [greatoutdoors] SET QUERY_STORE (OPERATION_MODE = READ_WRITE, CLEANUP_POLICY = (STALE_QUERY_THRESHOLD_DAYS = 30), DATA_FLUSH_INTERVAL_SECONDS = 900, INTERVAL_LENGTH_MINUTES = 60, MAX_STORAGE_SIZE_MB = 1000, QUERY_CAPTURE_MODE = AUTO, SIZE_BASED_CLEANUP_MODE = AUTO, MAX_PLANS_PER_QUERY = 200, WAIT_STATS_CAPTURE_MODE = ON)
GO
USE [greatoutdoors]
GO
/****** Object:  Table [dbo].[AGE_GROUP]    Script Date: 5-4-2024 00:18:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[AGE_GROUP](
	[AGE_GROUP_CODE] [int] NOT NULL,
	[UPPER_AGE] [int] NULL,
	[LOWER_AGE] [int] NULL,
 CONSTRAINT [PK_AGE_GROUP] PRIMARY KEY CLUSTERED 
(
	[AGE_GROUP_CODE] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[country]    Script Date: 5-4-2024 00:18:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[country](
	[COUNTRY_CODE] [int] NOT NULL,
	[LANGUAGE] [varchar](50) NULL,
	[CURRENCY_NAME] [varchar](50) NULL,
	[COUNTRY_EN] [varchar](50) NULL,
	[FLAG_IMAGE] [varchar](50) NULL,
	[SALES_TERRITORY_CODE] [int] NULL,
 CONSTRAINT [PK_country] PRIMARY KEY CLUSTERED 
(
	[COUNTRY_CODE] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[course]    Script Date: 5-4-2024 00:18:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[course](
	[course_code] [int] NOT NULL,
	[course_description] [varchar](255) NULL,
 CONSTRAINT [PK_course] PRIMARY KEY CLUSTERED 
(
	[course_code] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[date]    Script Date: 5-4-2024 00:18:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[date](
	[YEAR] [int] NULL,
	[MONTH] [int] NULL,
	[DAY] [int] NULL,
	[DATE] [date] NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[DAY]    Script Date: 5-4-2024 00:18:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[DAY](
	[DAY] [int] NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[MONTH]    Script Date: 5-4-2024 00:18:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[MONTH](
	[MONTH] [nchar](10) NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[order_method]    Script Date: 5-4-2024 00:18:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[order_method](
	[order_method_code] [int] NOT NULL,
	[order_method_name] [varchar](255) NULL,
 CONSTRAINT [PK_order_method] PRIMARY KEY CLUSTERED 
(
	[order_method_code] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[orders]    Script Date: 5-4-2024 00:18:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[orders](
	[order_number] [int] NOT NULL,
	[retailer_name] [varchar](255) NULL,
	[order_date] [date] NULL,
	[order_day] [int] NULL,
	[order_month] [int] NULL,
	[order_year] [int] NULL,
	[order_detail_code] [int] NOT NULL,
	[order_detail_product_number] [int] NULL,
	[order_detail_quantity] [int] NULL,
	[order_detail_unit_cost] [decimal](18, 0) NULL,
	[order_detail_unit_price] [decimal](18, 0) NULL,
	[order_detail_unit_sale_price] [decimal](18, 0) NULL,
	[return_code] [int] NULL,
	[return_date] [date] NULL,
	[return_reason_code] [int] NULL,
	[return_quantity] [int] NULL,
	[order_method_code] [int] NULL,
	[sales_staff_code_fk] [int] NULL,
	[sales_branch_code] [int] NULL,
	[retailer_site_code] [int] NULL,
	[sales_staff_code_fsk] [int] IDENTITY(1,1) NOT NULL,
 CONSTRAINT [PK_orders] PRIMARY KEY CLUSTERED 
(
	[order_number] ASC,
	[order_detail_code] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Product]    Script Date: 5-4-2024 00:18:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Product](
	[PRODUCT_NUMBER] [int] NOT NULL,
	[PRODUCT_NAME] [varchar](255) NULL,
	[INTRODUCTION_DATE_date] [date] NULL,
	[PRODUCT_TYPE_code] [int] NULL,
	[PRODUCT_TYPE_name] [varchar](255) NULL,
	[PRODUCT_LINE_code] [int] NULL,
	[PRODUCT_LINE_name] [varchar](255) NULL,
	[PRODUCTION_COST_number] [int] NULL,
	[MARGIN_number] [decimal](18, 0) NULL,
	[PRODUCT_IMAGE_image] [varchar](255) NULL,
	[LANGUAGE_language] [varchar](255) NULL,
	[DESCRIPTION_description] [varchar](255) NULL,
 CONSTRAINT [PK_Product] PRIMARY KEY CLUSTERED 
(
	[PRODUCT_NUMBER] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Retailer]    Script Date: 5-4-2024 00:18:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Retailer](
	[RETAILER_code] [nchar](10) NULL,
	[RETAILER_company_name] [nchar](10) NULL,
	[RETAILER_TYPE_code] [nchar](10) NULL,
	[RETAILER_TYPE_name] [nchar](10) NULL,
	[RETAILER_SEGMENT_segment_code] [nchar](10) NULL,
	[RETAILER_SEGMENT_language] [nchar](10) NULL,
	[RETAILER_SEGMENT_segment_name] [nchar](10) NULL,
	[RETAILER_SEGMENT_segment_description] [nchar](10) NULL,
	[RETAILER_HEADQUARTERS_name] [nchar](10) NULL,
	[RETAILER_HEADQUARTERS_address1] [nchar](10) NULL,
	[RETAILER_HEADQUARTERS_address2] [nchar](10) NULL,
	[RETAILER_HEADQUARTERS_city] [nchar](10) NULL,
	[RETAILER_HEADQUARTERS_region] [nchar](10) NULL,
	[RETAILER_HEADQUARTERS_country_code] [nchar](10) NULL,
	[RETAILER_HEADQUARTERS_country_flag_image] [nchar](10) NULL,
	[RETAILER_HEADQUARTERS_country_en] [nchar](10) NULL,
	[RETAILER_HEADQUARTERS_country_sales_territory_code] [nchar](10) NULL,
	[RETAILER_HEADQUARTERS_country_sales_territory_name] [nchar](10) NULL,
	[RETAILER_HEADQUARTERS_phone] [nchar](10) NULL,
	[RETAILER_HEADQUARTERS_fax] [nchar](10) NULL,
	[RETAILER_HEADQUARTERS_postal_zone] [nchar](10) NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[retailer_site]    Script Date: 5-4-2024 00:18:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[retailer_site](
	[COUNTRY_code] [int] NULL,
	[REGION_name] [varchar](255) NULL,
	[CITY_name] [varchar](255) NULL,
	[address1] [varchar](255) NULL,
	[address2] [varchar](255) NULL,
	[ACTIVE_INDICATOR_code] [smallint] NULL,
	[POSTAL_ZONE_code] [varchar](255) NULL,
	[RETAILER_TYPE_code] [int] NULL,
	[retailer_type_en] [varchar](255) NULL,
	[RETAILER_code] [int] NULL,
	[company_name] [varchar](255) NULL,
	[retailer_name] [varchar](255) NULL,
	[RETAILER_CONTACT_code] [int] NULL,
	[RETAILER_SITE_code] [int] NOT NULL,
	[retailer_headquarters_phone] [varchar](255) NULL,
	[retailer_headquarters_fax] [varchar](255) NULL,
	[retailer_headquarters_segment_code] [int] NULL,
 CONSTRAINT [PK_retailer_site] PRIMARY KEY CLUSTERED 
(
	[RETAILER_SITE_code] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[sales_branch]    Script Date: 5-4-2024 00:18:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[sales_branch](
	[SALES_BRANCH_CODE] [int] NOT NULL,
	[ADDRESS1] [varchar](255) NULL,
	[ADDRESS2] [varchar](255) NULL,
	[CITY] [varchar](255) NULL,
	[REGION] [varchar](255) NULL,
	[POSTAL_ZONE] [varchar](255) NULL,
	[COUNTRY_CODE] [int] NULL,
 CONSTRAINT [PK_sales_branch] PRIMARY KEY CLUSTERED 
(
	[SALES_BRANCH_CODE] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[sales_staff]    Script Date: 5-4-2024 00:18:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[sales_staff](
	[SALES_STAFF_CODE_PK] [int] NOT NULL,
	[FIRST_NAME] [varchar](255) NULL,
	[LAST_NAME] [varchar](255) NULL,
	[POSITION_EN] [varchar](255) NULL,
	[WORK_PHONE] [varchar](255) NULL,
	[EXTENSION] [varchar](255) NULL,
	[FAX] [varchar](255) NULL,
	[EMAIL] [varchar](255) NULL,
	[DATE_HIRED_DATE] [date] NULL,
	[SALES_BRANCH_CODE] [int] NULL,
	[MANAGER_CODE] [int] NULL,
	[timestmp] [datetime] NULL,
	[SALES_STAFF_CODE_SK] [int] IDENTITY(1,1) NOT NULL,
 CONSTRAINT [PK_sales_staff_1] PRIMARY KEY CLUSTERED 
(
	[SALES_STAFF_CODE_SK] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[SALES_TargetData]    Script Date: 5-4-2024 00:18:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[SALES_TargetData](
	[SALES_Target_Id] [int] NOT NULL,
	[SALES_STAFF_CODE] [int] NULL,
	[SALES_YEAR] [int] NULL,
	[SALES_PERIOD] [int] NULL,
	[RETAILER_NAME] [varchar](255) NULL,
	[PRODUCT_NUMBER] [int] NULL,
	[SALES_TARGET] [int] NULL,
	[RETAILER_CODE] [int] NULL,
 CONSTRAINT [PK_SALES_TargetData] PRIMARY KEY CLUSTERED 
(
	[SALES_Target_Id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[SALESDATA]    Script Date: 5-4-2024 00:18:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[SALESDATA](
	[PRODUCT_NUMBER] [int] NULL,
	[FORECAST_MONTH] [int] NULL,
	[FORECAST_YEAR] [int] NULL,
	[INVENTORY_MONTH] [int] NULL,
	[INVENTORY_YEAR] [int] NULL,
	[INVENTORY_COUNT] [int] NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[satisfaction]    Script Date: 5-4-2024 00:18:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[satisfaction](
	[year] [int] NOT NULL,
	[sales_staff_code] [int] NOT NULL,
	[satisfaction_type_code] [int] NULL,
 CONSTRAINT [PK_satisfaction] PRIMARY KEY CLUSTERED 
(
	[year] ASC,
	[sales_staff_code] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[satisfaction_type]    Script Date: 5-4-2024 00:18:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[satisfaction_type](
	[satisfaction_type_code] [int] NOT NULL,
	[satisfaction_type_description] [varchar](255) NULL,
 CONSTRAINT [PK_satisfaction_type] PRIMARY KEY CLUSTERED 
(
	[satisfaction_type_code] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[training]    Script Date: 5-4-2024 00:18:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[training](
	[YEAR] [int] NULL,
	[SALES_STAFF_CODE] [int] NOT NULL,
	[COURSE_CODE] [int] NOT NULL,
 CONSTRAINT [PK_training] PRIMARY KEY CLUSTERED 
(
	[SALES_STAFF_CODE] ASC,
	[COURSE_CODE] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[YEAR]    Script Date: 5-4-2024 00:18:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[YEAR](
	[YEAR] [nchar](10) NULL
) ON [PRIMARY]
GO
ALTER TABLE [dbo].[sales_staff] ADD  CONSTRAINT [DF_sales_staff_TIMESTAMP]  DEFAULT (getdate()) FOR [timestmp]
GO
USE [master]
GO
ALTER DATABASE [greatoutdoors] SET  READ_WRITE 
GO
