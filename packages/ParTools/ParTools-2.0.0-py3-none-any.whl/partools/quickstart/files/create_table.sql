BEGIN
	BEGIN
		EXECUTE IMMEDIATE 'DROP TABLE @@TABLE_NAME@@';
		EXCEPTION
			WHEN OTHERS THEN
				IF sqlcode != -0942 THEN RAISE; END IF;
	END;
	EXECUTE IMMEDIATE 'CREATE TABLE @@TABLE_NAME@@ (
		"AFFAIRE" VARCHAR2(8 BYTE), 
		"DEM_ID" VARCHAR2(9 BYTE),
		"PRM" VARCHAR2(14 BYTE)
	)';
	COMMIT;
END;
