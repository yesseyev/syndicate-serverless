from dataclasses import dataclass
from datetime import date, time


@dataclass
class TableData:
	id: int  # int
	number: int  # int, number of the table
	places: int  # int, amount of people to sit at the table
	isVip: bool  # boolean, is the table in the VIP hall
	minOrder: int | None  # optional. int, table deposit required to book it


@dataclass
class ReservationData:
	tableNumber: int  # int, number of the table
	clientName: str  # string
	phoneNumber: str  # string
	date: str  # string in yyyy-MM-dd format
	slotTimeStart: str  # string in "HH:MM" format, like "13:00",
	slotTimeEnd: str  # string in "HH:MM" format, like "15:00"

	def __post_init__(self):
		date.fromisoformat(self.date)
		time.fromisoformat(self.slotTimeStart)
		time.fromisoformat(self.slotTimeEnd)
