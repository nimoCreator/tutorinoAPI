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

        [HttpGet]
        [Route("getAllOffers")]
        public String GetOffers(Offers offerDesc)
        {
            int choosenSubject;
            switch(offerDesc.SubjectName){
                case "math":
                    choosenSubject = 0;
                    break;
                case "phys":
                    choosenSubject = 1;
                    break;
                case "chem":
                    choosenSubject = 2;
                    break;
                case "bio":
                    choosenSubject = 3;
                    break;
                case "hist":
                    choosenSubject = 4;
                    break;
                case "geo":
                    choosenSubject = 5;
                    break;
                case "eng":
                    choosenSubject = 6;
                    break;
                default:
                    choosenSubject = 7;
                    break;
            }
            SqlConnection con = new SqlConnection(configuration.GetConnectionString("AppCon").ToString());
            SqlDataAdapter data;
            if(choosenSubject == 7){
                data = new SqlDataAdapter("Select * from offers", con);
            }
            else{
                data = new SqlDataAdapter("Select * from offers where sid ="+choosenSubject, con);
            }
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
    
        
        [HttpGet]
        public String GetOffer(OfferPrint offerID){
            SqlConnection con = new SqlConnection(configuration.GetConnectionString("AppCon").ToString());
            SqlDataAdapter data = new SqlDataAdapter("Select * from offers where id="+offerID.id, con);
            DataTable dataTable = new DataTable();
            data.Fill(dataTable);
            OfferInfo offer = new OfferInfo();
            if (dataTable.Rows.Count > 0)
            {  
                offer.id = Convert.ToInt32(dataTable.Rows[0]["oid"]);
                offer.kuid = Convert.ToInt32(dataTable.Rows[0]["kuid"]);
                offer.sid = Convert.ToInt32(dataTable.Rows[0]["sid"]);
                offer.price = Convert.ToDouble(dataTable.Rows[0]["oid"]);
                offer.desc = Convert.ToString(dataTable.Rows[0]["desc"]);
                return JsonConvert.SerializeObject(offer);
            }
            else
            {
                return JsonConvert.SerializeObject(new Response(100,"No data found"));
            }
        }
    }     
}
