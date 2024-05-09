-- Script ranks country origins of bands, ordered by 
-- number of 'non-unique' fans
-- Column names: origin and nb_fans
SELECT origin, SUM(fans) AS nb_fans
    FROM metal_bands
    GROUP BY origin
    ORDER BY nb_fans DESC;
