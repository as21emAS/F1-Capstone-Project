export default function Dashboard() {
  /* testing .env */
  console.log("Jolpica URL:", import.meta.env.VITE_JOLPICA_BASE_URL);
  return (
    <div className="flex min-h-screen w-full items-center justify-center bg-f1-black m-0">
      <h1 className="font-racing text-5xl text-f1-red">
      	Welcome to the F1 Dashboard
      </h1>
      <h2 className="font-inter text-3xl text-redbull-blue ml-8">
      	This is going to be great. Just you wait
      </h2>
    </div>
  );
}
