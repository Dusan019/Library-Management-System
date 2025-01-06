DELIMITER $$

CREATE TRIGGER update_availability_before_update
BEFORE UPDATE ON books
FOR EACH ROW
BEGIN
    -- Check if quantity is updated and adjust availability accordingly
    IF NEW.quantity > 0 THEN
        SET NEW.available = TRUE;
    ELSE
        SET NEW.available = FALSE;
    END IF;
END$$

DELIMITER ;
