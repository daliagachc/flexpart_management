#!/bin/bash
#SBATCH -e ./error%j.txt
#SBATCH -o ./output%j.txt
#SBATCH -J flex
#SBATCH -n {SBATCH_N}
#SBATCH -t {SBATCH_T}
#SBATCH -p {SBATCH_P}
#SBATCH --mem-per-cpu={SBATCH_M}
#SBATCH --mail-type=END
#SBATCH --mail-user=diego.aliaga@helsinki.fi

# first set the environemt
export NETCDF=/appl/opt/netcdf4/gcc-7.3.0/intelmpi-18.0.2/4.6.1/
module purge
module load gcc/7.3.0  intelmpi/18.0.2 hdf5-par/1.8.20 netcdf4/4.6.1
export WRFIO_NCD_LARGE_FILE_SUPPORT=1

#flex_dir='/homeappl/home/aliagadi/appl_taito/flexpart/Src_flexwrf_v3.3.2-omp/examples'
flex_dir='/homeappl/home/aliagadi/appl_taito/FLEXPART-WRF_v3.3.2'
input_flex={FLX_INPUT_PATH_TAITO}
cd $flex_dir
#exe=flexwrf33_gnu_mpi
#exe=flexwrf33_gnu_omp
#exe=flexwrf33_gnu_serial
exe={FLX_EXE}
## run my MPI executable
srun $exe $input_flex
