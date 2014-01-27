delimiter '//'

CREATE PROCEDURE addcol() BEGIN
  IF NOT EXISTS(
    SELECT * FROM INFORMATION_SCHEMA.COLUMNS
    WHERE COLUMN_NAME='reason' AND TABLE_NAME='visits' AND TABLE_SCHEMA='schema'
  )
  THEN
    ALTER TABLE visits ADD COLUMN reason VARCHAR(255) NOT NULL DEFAULT '';
  END IF;
END;

//

delimiter ';'

CALL addcol();

DROP PROCEDURE addcol;