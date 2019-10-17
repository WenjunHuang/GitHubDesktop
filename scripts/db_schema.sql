create if not exists table t_key_value_string
(
	key varchar(64) not null constraint t_key_value_string_pk primary key,
	value varchar(2048) not null
);
