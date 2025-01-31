CREATE TABLE "users" (
    "id" INTEGER PRIMARY KEY,
    "name" VARCHAR NOT NULL,
    "email" VARCHAR NOT NULL UNIQUE,
    "role" VARCHAR NOT NULL DEFAULT 'user' CHECK(role IN ('user', 'admin'))
);

CREATE TABLE "storages" (
    "id" INTEGER PRIMARY KEY,
    "user_id" INTEGER NOT NULL,
    "description" VARCHAR DEFAULT 'storage {id}',
    FOREIGN KEY("user_id") REFERENCES "users"("id") ON DELETE CASCADE
);

CREATE TABLE "zones" (
    "id" INTEGER PRIMARY KEY,
    "storage_id" INTEGER NOT NULL,
    "description" VARCHAR NOT NULL DEFAULT 'zone {id}',
    FOREIGN KEY("storage_id") REFERENCES "storages"("id") ON DELETE CASCADE
);

CREATE TABLE "gadget_types" (
    "id" INTEGER PRIMARY KEY,
    "name" VARCHAR NOT NULL UNIQUE
);

CREATE TABLE "gadgets" (
    "id" INTEGER PRIMARY KEY,
    "zone_id" INTEGER NOT NULL,
    "description" VARCHAR NOT NULL,
    "type_id" INTEGER NOT NULL,
    "status" VARCHAR DEFAULT 'inactive' CHECK(status IN ('active', 'inactive')),
    FOREIGN KEY("zone_id") REFERENCES "zones"("id") ON DELETE CASCADE,
    FOREIGN KEY("type_id") REFERENCES "gadget_types"("id") ON DELETE CASCADE
);

CREATE TABLE "sensors" (
    "id" INTEGER PRIMARY KEY,
    "gadget_id" INTEGER NOT NULL,
    "check_period" INTEGER NOT NULL DEFAULT 0,
    "check_time" TIMESTAMP NOT NULL,
    "curr_param" REAL,
    "is_active" BOOLEAN DEFAULT FALSE,
    "is_outdoor" BOOLEAN NOT NULL DEFAULT FALSE,
    FOREIGN KEY("gadget_id") REFERENCES "gadgets"("id") ON DELETE CASCADE
);

CREATE TABLE "regulators" (
    "id" INTEGER PRIMARY KEY,
    "gadget_id" INTEGER NOT NULL,
    "is_active" BOOLEAN NOT NULL DEFAULT FALSE,
    "on_off_timer" INTEGER,
    "work_time" INTEGER,
    FOREIGN KEY("gadget_id") REFERENCES "gadgets"("id") ON DELETE CASCADE
);

CREATE TABLE "params" (
    "id" INTEGER PRIMARY KEY,
    "gadget_id" INTEGER NOT NULL,
    "description" VARCHAR NOT NULL,
    "param_zone_curr" REAL,
    "param_max" REAL,
    "param_min" REAL,
    "outdoor_param" REAL,
    FOREIGN KEY("gadget_id") REFERENCES "gadgets"("id") ON DELETE CASCADE
);

CREATE TABLE "sensor_data" (
    "id" INTEGER PRIMARY KEY,
    "sensor_id" INTEGER NOT NULL,
    "timestamp" TIMESTAMP NOT NULL,
    "temperature" REAL,
    "humidity" REAL,
    FOREIGN KEY("sensor_id") REFERENCES "sensors"("id") ON DELETE CASCADE
);

CREATE TABLE "regulator_history" (
    "id" INTEGER PRIMARY KEY,
    "regulator_id" INTEGER NOT NULL,
    "timestamp" TIMESTAMP NOT NULL,
    "status" VARCHAR(10) NOT NULL CHECK (status IN ('on', 'off')),
    FOREIGN KEY("regulator_id") REFERENCES "regulators"("id") ON DELETE CASCADE
);

CREATE TABLE "environmental_parameters" (
    "id" INTEGER PRIMARY KEY,
    "zone_id" INTEGER,
    "storage_id" INTEGER,
    "timestamp" TIMESTAMP NOT NULL,
    "temperature" REAL,
    "humidity" REAL,
    FOREIGN KEY("zone_id") REFERENCES "zones"("id") ON DELETE CASCADE,
    FOREIGN KEY("storage_id") REFERENCES "storages"("id") ON DELETE CASCADE
);
