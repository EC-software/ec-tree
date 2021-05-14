CREATE TABLE files (
  filename varchar PRIMARY KEY NOT NULL,
  filetime varchar NOT NULL,
  filesize integer NOT NULL,
  shorthash varchar NOT NULL,
  longhash varchar NOT NULL,
  scantime varchar NOT NULL
);
