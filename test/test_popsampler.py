
import popsampler

zone_sample_rate_file = "zone_sample_rate.csv"
hh_file = "households.csv"
hh_out_file = "households_out.csv"
per_file = "persons.csv"
per_out_file = "persons_out.csv"
hh_zone_field = "hhtaz"
zone_field = "zone_id"
use_income_bins = True
use_size_bins = True
use_worker_bins = False
income_field = "hhincome"
size_field = "hhsize"
workers_field = "hwkrs"
income_bin_1_max = 33333
income_bin_2_max = 66666
income_bin_3_max = 99999
hh_exp_fac_field = "hhexpfac"
hh_hh_id_field = "hhno"
per_hh_id_field = "hhno"

popsampler.run(zone_sample_rate_file, hh_file, hh_out_file, per_file, 
               per_out_file, hh_zone_field, zone_field, use_income_bins, 
               use_size_bins, use_worker_bins, income_field, size_field, 
               workers_field, income_bin_1_max, income_bin_2_max, income_bin_3_max,
               hh_exp_fac_field, hh_hh_id_field, per_hh_id_field)
