for f in *.jpg ; do montage -label orig $f -label east ../res_base/$f -label east_us ../res_am6/$f -label east_cas ../res_cas/$f -label east_us_cas ../res_am6_cas/$f -border 5 -tile 5x1 -geometry 256x256 ../montage/$f ; done