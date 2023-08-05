# Copyright (C) 2019 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.exceptions import ValidationError
from odoo.tests.common import Form, TransactionCase


class FSMLocation(TransactionCase):
    def setUp(self):
        super(FSMLocation, self).setUp()
        self.Location = self.env["fsm.location"]
        self.Equipment = self.env["fsm.equipment"]
        self.test_location = self.env.ref("fieldservice.test_location")
        self.location_1 = self.env.ref("fieldservice.location_1")
        self.location_2 = self.env.ref("fieldservice.location_2")
        self.location_3 = self.env.ref("fieldservice.location_3")
        self.test_territory = self.env.ref("base_territory.test_territory")
        self.test_loc_partner = self.env.ref("fieldservice.test_loc_partner")
        self.location_partner_1 = self.env.ref("fieldservice.location_partner_1")
        self.location_partner_2 = self.env.ref("fieldservice.location_partner_2")
        self.location_partner_3 = self.env.ref("fieldservice.location_partner_3")

    def test_fsm_location(self):
        """Test createing new location
        - Onchange parent, will get all parent info
        - Default stage
        - Change stage
        - Create fsm.location.person if auto_populate_persons_on_location
        """
        # Create an equipment
        view_id = "fieldservice.fsm_location_form_view"
        with Form(self.Location, view=view_id) as f:
            f.name = "Child Location"
            f.fsm_parent_id = self.test_location
        location = f.save()
        # Test child location equal to parent location
        for x in [
            "owner_id",
            "contact_id",
            "direction",
            "street",
            "street2",
            "city",
            "zip",
            "state_id",
            "country_id",
            "tz",
            "territory_id",
        ]:
            self.assertEqual(location[x], self.test_location[x])

        # Test initial stage
        self.assertEqual(
            location.stage_id, self.env.ref("fieldservice.location_stage_1")
        )
        # Test change state
        location.next_stage()
        self.assertEqual(
            location.stage_id, self.env.ref("fieldservice.location_stage_2")
        )
        location.next_stage()
        self.assertEqual(
            location.stage_id, self.env.ref("fieldservice.location_stage_3")
        )
        self.assertTrue(location.hide)  # hide as max stage
        location.previous_stage()
        self.assertEqual(
            location.stage_id, self.env.ref("fieldservice.location_stage_2")
        )
        # Test create fsm.location.person, when has if territory has person_ids
        self.env.user.company_id.auto_populate_persons_on_location = True
        person_ids = [
            self.env.ref("fieldservice.person_1").id,
            self.env.ref("fieldservice.person_2").id,
            self.env.ref("fieldservice.person_3").id,
        ]
        self.test_territory.write({"person_ids": [(6, 0, person_ids)]})
        location.territory_id = self.test_territory
        self.assertEqual(len(location.person_ids), 0)
        location._onchange_territory_id()
        self.assertEqual(len(location.person_ids), 3)
        location.owner_id.action_open_owned_locations()

    def test_fsm_multi_sublocation(self):
        """Test create location with many sub locations
        - Test recursion exceptoin
        - Test count all equipments, contacts, sublocations
        """
        # Test Location > Location 1 > Location 2 > Location 3
        self.location_3.fsm_parent_id = self.location_2
        self.location_2.fsm_parent_id = self.location_1
        self.location_1.fsm_parent_id = self.test_location
        # Test sublocation_count of each level
        self.assertEqual(
            (
                self.test_location.sublocation_count,
                self.location_1.sublocation_count,
                self.location_2.sublocation_count,
                self.location_3.sublocation_count,
            ),
            (3, 2, 1, 0),
        )
        loc_ids = self.test_location.action_view_sublocation()["domain"][0][2]
        loc_1_ids = self.location_1.action_view_sublocation()["domain"][0][2]
        loc_2_ids = [self.location_2.action_view_sublocation()["res_id"]]
        loc_3_ids = self.location_3.action_view_sublocation()["domain"][0][2]
        self.assertEqual(
            (len(loc_ids), len(loc_1_ids), len(loc_2_ids), len(loc_3_ids)), (3, 2, 1, 0)
        )

        # Test recursion exception
        with self.assertRaises(ValidationError):
            self.test_location.fsm_parent_id = self.location_3
        self.test_location.fsm_parent_id = False  # Set back

        # Add equipments on each locations, and test counting
        location_vs_num_eq = {
            self.test_location.id: 1,  # Topup = 9
            self.location_1.id: 1,  # Topup = 8
            self.location_2.id: 5,  # Topup = 7
            self.location_3.id: 2,
        }  # Topup = 2
        for loc_id, num_eq in location_vs_num_eq.items():
            for i in range(num_eq):
                self.Equipment.create(
                    {
                        "name": "Eq-{}-{}".format(str(loc_id), str(i + 1)),
                        "location_id": loc_id,
                        "current_location_id": loc_id,
                    }
                )
        # Test valid equipments at each location
        self.assertEqual(
            (
                self.test_location.equipment_count,
                self.location_1.equipment_count,
                self.location_2.equipment_count,
                self.location_3.equipment_count,
            ),
            (9, 8, 7, 2),
        )  # !!
        # Test smart button to open equipment
        loc_eq_ids = self.test_location.action_view_equipment()["domain"][0][2]
        loc_1_eq_ids = self.location_1.action_view_equipment()["domain"][0][2]
        loc_2_eq_ids = self.location_2.action_view_equipment()["domain"][0][2]
        loc_3_eq_ids = self.location_3.action_view_equipment()["domain"][0][2]
        self.assertEqual(
            (len(loc_eq_ids), len(loc_1_eq_ids), len(loc_2_eq_ids), len(loc_3_eq_ids)),
            (9, 8, 7, 2),
        )

        # Set service_location_id, on relavant res.partner, test contact count
        self.test_loc_partner.service_location_id = self.test_location
        self.location_partner_1.service_location_id = self.location_1
        self.location_partner_2.service_location_id = self.location_2
        self.location_partner_3.service_location_id = self.location_3
        # Test valid contacts at each location
        self.assertEqual(
            (
                self.test_location.contact_count,
                self.location_1.contact_count,
                self.location_2.contact_count,
                self.location_3.contact_count,
            ),
            (4, 3, 2, 1),
        )
        # Test smart button to open contacts
        cont_ids = self.test_location.action_view_contacts()["domain"][0][2]
        cont_1_ids = self.location_1.action_view_contacts()["domain"][0][2]
        cont_2_ids = self.location_2.action_view_contacts()["domain"][0][2]
        cont_3_ids = [self.location_3.action_view_contacts()["res_id"]]
        self.assertEqual(
            (len(cont_ids), len(cont_1_ids), len(cont_2_ids), len(cont_3_ids)),
            (4, 3, 2, 1),
        )

    def test_convert_partner_to_fsm_location(self):
        """
        FSM Location can be created from the res.partner form
        like invoice addresses or delivery addresses.

        child of partner with type = fsm_location
        """
        self.test_partner = self.env.ref("fieldservice.test_partner")
        # ensure no regression on classic types
        contact = self.env["res.partner"].create(
            {
                "parent_id": self.test_partner.id,
                "name": "A contact",
                "type": "contact",
            }
        )
        self.assertFalse(contact.fsm_location)
        no_type = self.env["res.partner"].create(
            {
                "parent_id": self.test_partner.id,
                "name": "A contact",
            }
        )
        self.assertFalse(no_type.fsm_location)

        # test with type = fsm_location
        vals = {
            "parent_id": self.test_partner.id,
            "name": "A location",
            "type": "fsm_location",
        }
        child_loc = self.env["res.partner"].create(vals)

        self.assertTrue(child_loc.fsm_location, "fsm_location Flag should be set")
        self.assertTrue(
            child_loc.fsm_location_id.exists(), "fsm.location should exists"
        )
        self.assertEqual(
            child_loc.fsm_location_id.partner_id,
            child_loc,
            "ensure circular references",
        )

    def test_convert_partner_to_fsm_location_multi(self):
        """
        Ensure behavior in create_multi
        """
        self.test_partner = self.env.ref("fieldservice.test_partner")
        vals = [
            {"parent_id": self.test_partner.id, "type": "invoice", "name": "contact"},
            {
                "parent_id": self.test_partner.id,
                "type": "fsm_location",
                "name": "location",
            },
        ]
        children_loc = self.env["res.partner"].create(vals)
        self.assertEqual(len(children_loc.filtered("fsm_location")), 1)

        # ensure archive is still possible
        children_loc.action_archive()
        self.assertTrue(
            self.env["res.partner"].search(
                [("active", "=", False), ("id", "in", children_loc.ids)]
            )
        )
