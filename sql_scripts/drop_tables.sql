DO $$
DECLARE
    r RECORD;
BEGIN
    -- Для каждой таблицы в схеме public
    FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
        EXECUTE 'DROP TABLE IF EXISTS public.' || quote_ident(r.tablename) || ' CASCADE';
    END LOOP;
END $$;

DROP TYPE IF EXISTS transaction_type_enum;


