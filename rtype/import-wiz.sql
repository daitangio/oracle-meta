
-- Import wiz load data 
attach database ":memory:" as loader_area;

.mode csv
.separator ;
.import C:/giorgi/nttdata/std_cost_2014.csv std_cost
-- select * from std_cost;
