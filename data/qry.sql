SELECT
    cn_salge.SAL_ANOP AS ANNIO
    ,cn_salge.SAL_MESP AS MES
    ,CN_CUENT.CUE_NO01 AS NOMNIVEL1
    ,CN_CUENT.CUE_NO02 AS NOMNIVEL2
    ,CN_CUENT.CUE_NO03 AS NOMNIVEL3
    ,CAST(ROUND(CASE
        WHEN CN_CUENT.CUE_NATU ='D' THEN cn_salge.SCE_VADB - cn_salge.SCE_VACR 
        WHEN CN_CUENT.CUE_NATU ='C' THEN cn_salge.SCE_VACR - cn_salge.SCE_VADB
        ELSE 0 END, 0) AS numeric) AS Saldo
FROM [Stage].[Seven].[cn_salge]
INNER JOIN [Stage].[Seven].CN_CUENT ON CN_CUENT.CUE_CONT = cn_salge.CUE_CONT
                                    AND CN_CUENT.EMP_CODI = cn_salge.EMP_CODI