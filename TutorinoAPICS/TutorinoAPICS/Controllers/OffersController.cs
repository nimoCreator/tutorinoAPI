using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Newtonsoft.Json;
using System.Data.SqlClient;
using System.Data;
using TutorinoAPICS.Models;

namespace TutorinoAPICS.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class OffersController : ControllerBase
    {

        public readonly IConfiguration configuration;
        public OffersController(IConfiguration configuration)
        {
            this.configuration = configuration;
        }

        //In progress, Code 100 - No offers
        [HttpGet]
        [Route("getAllOffers")]
        public String GetOffers()
        {
            SqlConnection con = new SqlConnection(configuration.GetConnectionString("AppCon").ToString());
            SqlDataAdapter data = new SqlDataAdapter("Select * from offers", con);
            DataTable dataTable = new DataTable();
            data.Fill(dataTable);
            List<Offer> offers = new List<Offer>();
            if (dataTable.Rows.Count > 0)
            {
                for (int i = 0; i < dataTable.Rows.Count; i++)
                {
                    Offer ofr = new Offer();
                    ofr.id = Convert.ToInt32(dataTable.Rows[i]["oid"]);
                    ofr.price = Convert.ToDouble(dataTable.Rows[i]["price"]);
                    ofr.description = Convert.ToString(dataTable.Rows[i]["desc"]);
                    offers.Add(ofr);
                }
            }
            if (offers.Count > 0)
            {
                return JsonConvert.SerializeObject(offers);
            }
            else
            {
                return JsonConvert.SerializeObject(new Response(100,"Empty"));
            }
        }

        //Codes 0 - Data added successfully, 100 - Other Error, 101 - User or Subject are not correct
        [HttpPost]
        [Route("addOffer")]
        public String AddOffer(OfferAdded newOffer)
        {
            SqlConnection con = new SqlConnection(configuration.GetConnectionString("AppCon").ToString());
            SqlCommand cmd = new SqlCommand("Insert into offers(kuid,sid,price,[desc]) values('" + newOffer.userID + "','" + newOffer.subjectID + "','" + newOffer.price + "','" + newOffer.description + "')", con);
            con.Open();
            int i;
            try
            {
                i = cmd.ExecuteNonQuery();
            } catch (Exception ex)
            {
                return JsonConvert.SerializeObject(new Response(101, "Error"));
            }
            con.Close();
            if (i > 0)
            {
                return JsonConvert.SerializeObject(new Response(0, "Data added"));
            }
            else
            {
                return JsonConvert.SerializeObject(new Response());
            }
        }

        [HttpPost]
        [Route("editOffer")]
        public String EditOffer(Offer offer)
        {
            
        }

        [HttpPost]
        [Route("deleteOffer")]
        public String DeleteOffer(OfferIDD offer)
        {
            
        }

        [HttpGet]
        [Route("getOffersByUserId")]
        public string GetOffersByUserId(OfferUID offer)
        {
            
        }

        [HttpGet]
        [Route("getOffersBySubjectId")]
        public string GetOffersBySubjectId(OfferSubject subject)
        {

        }

        [HttpGet]
        [Route("getOffersByUIdAndSId")]
        public string GetOffersByUIdAndSId(OfferID offer)
        {
            using (SqlConnection con = new SqlConnection(configuration.GetConnectionString("AppCon")))
            {
                string query = "SELECT * FROM offers WHERE kuid = @userId AND sid = @subjectId";
                using (SqlCommand cmd = new SqlCommand(query, con))
                {
                    cmd.Parameters.AddWithValue("@userId", offer.userID);
                    cmd.Parameters.AddWithValue("@subjectId", offer.subjectID);

                    SqlDataAdapter data = new SqlDataAdapter(cmd);
                    DataTable dataTable = new DataTable();
                    data.Fill(dataTable);
                    List<Offer> offers = new List<Offer>();

                    if (dataTable.Rows.Count > 0)
                    {
                        foreach (DataRow row in dataTable.Rows)
                        {
                            Offer ofr = new Offer
                 
                            {
                                id = Convert.ToInt32(row["oid"]),
                                userID = Convert.ToInt32(row["kuid"]),
                                subjectID = Convert.ToInt32(row["sid"]),
                                price = Convert.ToDouble(row["price"]),
                                description = Convert.ToString(row["desc"])
                            };
                            offers.Add(ofr);
                        }
                    }

                    if (offers.Count > 0)
                    {
                        return JsonConvert.SerializeObject(offers);
                    }
                    else
                    {
                        return JsonConvert.SerializeObject(new Response(100, "No offers found for the specified user ID and subject ID"));
                    }
                }
            }
        }
    }
}
