DO $$
DECLARE
    seq RECORD;
BEGIN
    FOR seq IN
        SELECT
            pg_class.relname AS sequence_name,
            t.relname AS table_name,
            a.attname AS column_name
        FROM
            pg_class
        JOIN
            pg_depend ON pg_depend.objid = pg_class.oid
        JOIN
            pg_class t ON pg_depend.refobjid = t.oid
        JOIN
            pg_attribute a ON a.attrelid = t.oid AND a.attnum = pg_depend.refobjsubid
        WHERE
            pg_class.relkind = 'S' -- Только sequences
            AND pg_depend.deptype = 'a' -- Только автогенерируемые по SERIAL/BIGSERIAL
    LOOP
        EXECUTE format(
            'SELECT setval(''%I'', COALESCE(MAX(%I), 1)) FROM %I',
            seq.sequence_name,
            seq.column_name,
            seq.table_name
        );
    END LOOP;
END $$;
