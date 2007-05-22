��    J      l  e   �      P  �   Q      l       �     �	     �	     �	     �	     �	  
   �	     �	  �   �	     �
     �
     �
     �
                              /     6     ;     B     I  	   \     f     i     p     ~     �  	   �     �  3  �     �     �     �  	     
             1     6     C     R     [     n     v     �     �     �     �  ,   �  :     4   Q  '   �     �  >   �  X   �  G   L  �   �  E   '     m     r     w          �  �   �  �   }  !       @  	   T     ^  $  d  �   �  >  >  �   }    �  	              9  %   S  "   y  	   �     �    �     �  	   �     �     �     �                    !     2     9     @     H     O     c     k     n     w     �     �     �     �  a  �  	               %     F     L     Y     p     w     �  	   �     �     �     �     �     �     �     	  .     :   L  6   �  '   �     �  J   �  l   8  R   �  �   �  J   �     �     �  
   �     �  
      �      �   �   7  �!     �"     �"     �"        8   $   B   >      )   6      *      7   J   C                  /   ,          	   
       ?                                       &   4       %   @           ;   E       .   3   H             :         (   +          G   #                         I      -              "   D       1       <                 '   F   0   5   A       =   2          9   !                  A Local Content object provides an storage for multilingual (and non multilingual) properties. It also helps to keep your content separated from the logic and the presentation. A Localizer object provides <em>locale folders</em>, each one associated with a language. It transparently adds a locale folder to the path so objects for that language will be used. It's useful to localize special objects like images, or specific logic (to format dates for example). A local folder is a generic solution to manage any kind of multingual objects, files, images, scripts, etc.. A message catalog stores messages and its translations to different languages. It provides the <tt>gettext</tt> method to get the right translation for a given message. Message catalogs are useful to translate the application interfaces (labels, buttons, etc..). Add Add Local Content Add Local Folder Add Localizer Add Message Catalog Attributes Basque Besides the title the header of a PO file stores more information, the name and the email address of the last translator, the email adress of the translation team and the charset. The forms below let to modify this information for each language. Catalan Change Charset Contents Default Delete Export File File / Language Filter Find French German Hide this language Hungarian Id Import Import/Export Japanese Language Languages Local properties Locale folders are useful to store special multilingual objects like images and specific logic. If used the <tt>Localizer</tt> object will transparently add the right locale folder to the url. If you want to use locale folders check the checkbox, otherwise uncheck it, then click the <tt>Change</tt> button. Messages Name Only untranslated messages Ownership Properties Results %d-%d of %d Save Save changes Saved changes. Security Show this language Spanish Team e-mail address There aren't attributes There aren't languages There aren't messages. There aren't properties. This <tt>%s</tt> object needs to be upgraded This <tt>Localizer</tt> object don't needs to be upgraded. This <tt>Localizer</tt> object needs to be upgraded. This object don't needs to be upgraded. Title To add a language select it and click the <tt>Add</tt> button. To add a new property enter its name, select its type and click the <tt>Add</tt> button. To add an attribute introduce its id and click the <tt>Add</tt> button. To delete a language check it and click the <tt>Delete</tt> button. To change the default language select it and click the <tt>Change</tt> button. To delete an attribute check it and click the <tt>Delete</tt> button. Type Undo Upgrade Use locale folders View With this form you can change the title of the message catalog. The title also is used as the value of the <tt>Project-Id-Version</tt> field in the header of the PO files, which are generated when the message catalog is exported. You can add new messages and translations importing a PO file. Enter the filename, select the language of the translations and click the <tt>Import</tt> button. You can export the messages and their translations to PO files. Check <tt>locale.pot</tt> to get only the messages, without their translations. Check any other option to get a PO file with the messages and their translations to the selected language. Then click the <tt>Export</tt> button. Your e-mail address Your name label Project-Id-Version: Localizer
POT-Creation-Date: 2002-09-10 14:09+CET
PO-Revision-Date: 2007-05-01 16:35+0100
Last-Translator: 
Language-Team: Portugu�s <luis727@gmail.com>
MIME-Version: 1.0
Content-Type: text/plain; charset=iso-8859-1
Content-Transfer-Encoding: 8bit
X-Generator: KBabel 0.8
 Um objeto de Conte�do Local prov� um armazenamento para propriedades multilinguais (e n�o multilinguais). Tamb�m ajuda a manter o seu conte�do separado da l�gica e da apresenta��o. Um objecto "Localizer" prov� <em>pastas de idioma</em>, cada uma associada com um idioma. Transparentemente adiciona uma pasta de idioma ao caminho de modo que objetos para aquele idioma ser�o utilizados. � �til localizar objectos especiais tais como imagens, ou alguma l�gica espec�fica (por exemplo, formatar datas). Uma pasta local � uma solu��o gen�rica para administrar qualquer tipo de objectos multilingues, arquivos, imagens, scripts, etc.. Um cat�logo de mensagens armazena mensagens e suas tradu��es para diferentes idiomas. Ele prov� o m�todo <tt>gettext</tt> afim de obter a tradu��o correta para uma dada mensagem. Cat�logos de mensagens s�o �teis para traduzir as interfaces da aplica��o (r�tulos, bot�es, etc..). Adicionar Adicionar Conte�do Local Adicionar uma Pasta Local Adicionar um inst�ncia do "Localizer" Adicionar um cat�logo de mensagens Atributos Basco Al�m do t�tulo, o cabe�alho de um arquivo PO armazena mais informa��o: o nome e o endere�o de email do �ltimo tradutor, o endere�o de email da equipa de tradu��o e o conjunto de caracteres (<em>charset</em>). Os formul�rios abaixo permitem modificar estas informa��es para cada idioma. Catal�o Modificar Conjunto de caracteres Conte�do Por defeito Remover Exportar Arquivo Arquivo / Idioma Filtro Buscar Franc�s Alem�o Ocultar este idioma H�ngaro Id Importar Importar/Exportar Japon�s Idioma Idiomas Propriedades Locais As pastas de idioma s�o �teis para armazenar objetos especiais multiliguais como imagens e l�gica espec�fica. Se utilizado, o objeto <tt>Localizer</tt> ir� transparentemente, adicionar a pasta de idioma correta � url. Se voc� quer utilizar pastas de idioma, indique na caixa de sele��o, caso contr�rio, n�o indique, e ent�o clique o bot�o <tt>Mudar</tt> Mensagens Nome Somente mensagens n�o traduzidas Posse Propriedades Resultados %d-%d de %d Salvar Salvar modifica��es Mudan�as guardadas Seguran�a Mostrar este idioma Espanhol Endere�o da equipa N�o h� atributos N�o h� idiomas N�o h� mensagens N�o h� propriedades Este objeto <tt>%s</tt> precisa ser atualizado Este objecto <tt>Localizer</tt> n�o precisa ser atualizado Este objecto <tt>Localizer</tt> precisa ser atualizado Este objeto n�o precisa ser atualizado. T�tulo Para adicionar um idioma, seleccione-o e clique o bot�o <tt>Adicionar</tt> Para adicionar uma nova propriedade entre seu nome, selecione seu tipo e clique no bot�o <tt>Adicionar</tt>. Para adicionar um atributo, introduza o seu ID e clique o bot�o <tt>Adicionar</tt> Para remover um idioma, seleccione-o e clique no bot�o <tt>Remover</tt> . Para modificar o idioma padr�o, selecione-o e clique <tt>Modificar</tt> Para remover um atributo, seleccione-o e clique o bot�o <tt>Adicionar</tt> Tipo Desfazer Actualizar Utilizar pastas de idioma Visualizar Com este formul�rio, pode mudar o t�tulo do cat�logo de mensagens. O t�tulo tamb�m � utilizado como o valor do campo <tt>Project-Id-Version</tt> no cabe�alho do arquivos PO, que s�o gerados quando o cat�logo de mensagens � exportado. Voc� pode adicionar novas mensagens e tradu��es importando um arquivo PO. Entre o nome do arquivo, selecione o idioma das tradu��es e clique o bot�o <tt>Importar</tt> Voc� pode exportar as mensagens e suas tradu��es para arquivos PO. Selecione <tt>locale.pot</tt> para exportar somente as mensagens, sem suas tradu��es. Selecione qualquer outra op��o para gerar um arquivo "PO" com as mensagens e suas tradu��es para o idioma selecionado. Ent�o clique o bot�o <tt>Exportar</tt>. Seu endere�o de email Seu nome r�tulo 