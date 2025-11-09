-- CREA LA BASE DE DATOS
CREATE DATABASE Test


-- USAMOS LA BASE DE DATOS CREADA Y SETEAMOS EL LENGUAJE
USE Test
SET LANGUAGE SPANISH



-- CREAR LAS TABLAS
CREATE TABLE Products (Id INT IDENTITY (1,1),
					   [Name] VARCHAR(75),
					   Price FLOAT,
					   Category_Id INT)

CREATE TABLE Categories (Id INT IDENTITY (1,1),
						 [Name] VARCHAR(75) 
						)

CREATE TABLE Inventory (Id INT IDENTITY (1,1),
					    [Name] VARCHAR(75),
					    Price FLOAT,
					    Category_Id INT)

-- CREAR LLAVES PRIMARIAS
ALTER TABLE Products
ADD CONSTRAINT PK_Id PRIMARY KEY (Id)

ALTER TABLE Categories
ADD CONSTRAINT PK_IdC PRIMARY KEY (Id)

ALTER TABLE Inventory
ADD CONSTRAINT PK_IdI PRIMARY KEY (Id)


-- CREAMOS LLAVE FORANEA DE LA TABLA CATEGORIES
ALTER TABLE Products
ADD CONSTRAINT FK_Category_Id FOREIGN KEY (Category_Id)
REFERENCES Categories (Id);


-- INSERTAMOS LOS DATOS INDICADOS
INSERT INTO Categories VALUES ('Electronicos')
INSERT INTO Categories VALUES ('Ropa')
INSERT INTO Categories VALUES ('Hogar')

INSERT INTO Products VALUES ('Laptop Acer','799.99','1') 
INSERT INTO Products VALUES ('Smartphone','499.99','1')
INSERT INTO Products VALUES ('Tablet Lenovo','299.99','1')


-- CONSULTA LOS PRODUCTOS DE LA TIENDA
SELECT		*
FROM		Products


-- ACTUALIZAR PRECIO DE LAPTOP ACER
UPDATE		Products
SET			Price = '999.99'
WHERE		[Name] = 'Laptop Acer'


-- ELIMINAR EL PRODUCTO LAPTOP ACER
DELETE FROM Products
WHERE		[Name] = 'Laptop Acer'


-- CONSULTA DE JOIN CON CATEGORIA
SELECT		A.Id AS [Id Producto],
			A.Name AS [Nombre Producto],
			A.Price AS [Precio Producto],
			B.Id AS [Id Categoria],
			B.Name AS [Nombre Categoria]
FROM		Products AS A INNER JOIN Categories AS B
			ON A.Category_Id = B.Id


-- TRIGGER DE INSERCIÓN EN INVENTARIO
CREATE TRIGGER		InventarioActual
ON		Products
AFTER INSERT
  AS
	BEGIN
		INSERT INTO Inventory
		SELECT		Name,
					Price,
					Category_Id
		FROM		Products
		WHERE		Name NOT IN (SELECT	Name
								 FROM	Inventory)

SELECT 'Se agregó un producto nuevo al inventario' AS [Mensaje]
END

-- INSERCÍÓN PARA VALIDACIÓN DE FUNCIONAMIENTO
INSERT INTO Products VALUES ('Samsung Galaxy S25 Ultra','999.99','1')


-- PROCEDIMIENTO ALMACENADO DE CONSULTA DE PRODUCTOS
CREATE PROCEDURE SP_ConsultaProductos
(
    @Id INT = NULL
)
AS
	BEGIN
		SELECT		COUNT(*) AS [Cantidad],
					Name AS [Producto]
        FROM		Products
        WHERE		Id = @id
		GROUP BY	Name
	END

-- EJECUCIÓN DE PRUEBA DE FUNCIONAMIENTO
EXEC SP_ConsultaProductos @id = 3