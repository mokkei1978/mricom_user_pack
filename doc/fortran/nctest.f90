!- netCDF をテストする：長さ 3 の変数を 1 つ持つ `test.nc` を書く
program nctest
  use netcdf
  implicit none
  integer :: ncid, dimid, varid, i
  real(4) :: x(3) = [(real(i), i = 1, 3)]
  call check(nf90_create("test.nc", NF90_NETCDF4, ncid))
  call check(nf90_def_dim(ncid, "x", 3, dimid))
  call check(nf90_def_var(ncid, "data", NF90_FLOAT, [dimid], varid))
  call check(nf90_enddef(ncid))
  call check(nf90_put_var(ncid, varid, x))
  call check(nf90_close(ncid))
  print *, "ok: ", trim(nf90_inq_libvers())
contains
  subroutine check(status)
    integer, intent(in) :: status
    if (status /= nf90_noerr) then
      print *, trim(nf90_strerror(status)); stop 1
    end if
  end subroutine check
end program nctest
