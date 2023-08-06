from pymongoose.mongo_types import Types, Schema

class RegistrationPhase (Schema):
	schema_name = "registrations.phases"

	competition = None

	name = None
	description = None

	price = None
	currency = None

	start_date = None
	end_date = None

	available = None
	sold = None

	def __init__ (self, **kwargs):
		self.schema = {
			"competition": {
				"type": Types.ObjectId,
				"ref": "competitions",
				"required": True
			},
			"name": {
				"type": Types.String,
				"required": True
			},
			"description": {
				"type": Types.String,
				"required": True
			},

			"price": {
				"type": Types.Number,
				"required": True
			},
			"currency": {
				"type": Types.ObjectId,
				"ref": "currencies",
				"required": True
			},

			"start_date": {
				"type": Types.Date,
				"required": True
			},
			"end_date": {
				"type": Types.Date,
				"required": True
			},

			"available": {
				"type": Types.Number,
				"required": True
			},
			"sold": {
				"typer": Types.Number,
				"default": 0
			}
		}

		super ().__init__ (self.schema_name, self.schema, kwargs)

	def __str__ (self):
		return f"RegistrationPhase: {self.id}"
