/*
CREATE TRIGGER update_Order_FSK_trigger
ON sales_staff
AFTER INSERT
AS
BEGIN
    DECLARE @latest_SK INT;

    -- Zoek de nieuwste sales_staff_code_sk
    SELECT @latest_SK = MAX(sales_staff_code_sk) FROM inserted;

    -- Update de Order-tabel met de nieuwste sales_staff_code_sk
    UPDATE orders
    SET orders.sales_staff_code_fsk = @latest_SK
    FROM Orders o
    INNER JOIN inserted i ON o.sales_staff_code_fk = i.sales_staff_code_pk;
END;
*/



CREATE TRIGGER update_fsk_after_order_insert
ON orders
AFTER INSERT
AS
BEGIN
    UPDATE o
    SET o.SALES_STAFF_CODE_FSK = ss.SALES_STAFF_CODE_SK
    FROM orders o
    INNER JOIN inserted i ON o.SALES_STAFF_CODE_FK = i.SALES_STAFF_CODE_FK
    INNER JOIN (
        SELECT sales_staff.SALES_STAFF_CODE_PK, MAX(sales_staff.SALES_STAFF_CODE_SK) AS MAX_SALES_STAFF_CODE_SK
        FROM sales_staff
        INNER JOIN inserted ON sales_staff.SALES_STAFF_CODE_PK = inserted.SALES_STAFF_CODE_FK
        WHERE sales_staff.timestmp <= inserted.tstamp
        GROUP BY sales_staff.SALES_STAFF_CODE_PK
    ) ss_max ON i.SALES_STAFF_CODE_FK = ss_max.SALES_STAFF_CODE_PK
    INNER JOIN sales_staff ss ON ss.SALES_STAFF_CODE_PK = ss_max.SALES_STAFF_CODE_PK AND ss.SALES_STAFF_CODE_SK = ss_max.MAX_SALES_STAFF_CODE_SK
    WHERE o.tstamp = i.tstamp;
END;