from platzabfrage import LectureHall

def make_rectangular_hall(name, rows, columns, elevated=False):
    
    rectangular_segment = LectureHall.Segment()

    for _ in range(rows):
        rectangular_segment._add_row_after(num_seats=columns, row_is_elevated=elevated)
    
    rectangular_hall = LectureHall(name=name, segments=[rectangular_segment], capacity=rows*columns)
    return rectangular_hall



if __name__ == '__main__':

    hs_8 = make_rectangular_hall("HS 8", 14,14, elevated=True)
    #print(hs_8.name,":\n")
    #for d in sorted(hs_8.segments[0].rows.keys()):
    #    print(d, hs_8.segments[0].rows[d]["seats"], '\n')

    hs_8.save_hall_as_json()
