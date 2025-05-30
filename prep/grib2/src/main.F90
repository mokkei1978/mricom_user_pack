program main
  use wgrib2api
  implicit none

  character(255) :: file_in  !- grib2 file (sample: MOVE-JPN SSH)

  real(4),allocatable :: r(:,:), lat(:,:), lon(:,:)
  integer             :: irtn = 99
  integer             :: iargc

  if ( iargc() < 1 ) then
    write(*,*) 'Usage: ./main FILE_IN'
    stop
  endif
  call getarg(1,file_in)

  irtn = grb2_mk_inv(trim(file_in),'a.inv')
!  write(6,*) 'irtn:',irtn
  irtn = grb2_inq(trim(file_in),'a.inv',':DSLM:surface:',':0-1 day ave fcst:', &
         data2=r, lat=lat, lon=lon)
  write(6,*) 'irtn:',irtn

  write(6,*) shape(lat)
!  write(6,*) lat(1423,1604)
  write(6,*) shape(lon)
!  write(6,*) lon(1423,1604)
  write(6,*) shape(r)
  write(6,*) r(1:10,1)

end program main
