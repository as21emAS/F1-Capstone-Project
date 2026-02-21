
DROP DATABASE IF EXISTS f1_predictor;
CREATE DATABASE f1_predictor;

\c f1_predictor;


\i schema.sql;
\i indexes.sql;